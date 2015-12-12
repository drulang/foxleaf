from __future__ import absolute_import
import subprocess
import os
import re

from bluebutter.celery import app
from cobalt import models
import requests


@app.task
def resize_profile_image(userid):
    """
    Resizes a profile image to the size 200x200 while keeping the aspect ratio
    intact
    """
    user =  models.User.objects.filter(id=userid).first()
    if user and user.profileimage:
        print("User and profileimage was found. Username; %s" % user.username)

        current_file = user.profileimage.relativepath
        print("Converting profileiamge: %s", current_file)

        current_filename, currentFileExt = os.path.splitext(current_file)
        new_file = current_filename + '.png'

        print("New File: %s", new_file)

        args = [
            "gm",
            "convert",
            current_file,
            "-scale",
            "200x200^",
            "-gravity",
            "center",
            "-extent",
            "200x200",
            new_file,
        ]

        returncode = subprocess.call(args) 

        if returncode == 0:
            user.profileimage.relativepath = new_file
            user.profileimage.save()
            os.remove(current_file)
            print("Successful")
        else:
            print("Error")

    else:
        print("Unable to find user and profile image")
        print("User: %s" % user)
    return "OK"

@app.task
def adjust_book_cover_url(bookid):
    """
    When books are added via the google search the book cover url is pretty small. 
    This task will find a higher quality cover.  This is needed until book covers
    are hosted locally
    """

    book =  models.Book.objects.filter(id=bookid).first()

    if not book:
        print("Unable to find book with id: %s" % bookid)
        return
    elif not book.coverurl:
        print("Book with id '%s' has no cover url" % bookid)
        return
    # Example
    # http://books.google.com/books/content?id=Z8LGFPb_hNkC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api

    #1. Determine if book cover is small
    url = book.coverurl
    preferred_zoom = "zoom=2"

    if 'zoom' not in url:
        url = url + "&zoom=2"
    elif preferred_zoom not in url:
        url = second_part = re.sub(r'zoom=[\d]+', 'zoom=2', url)

        resp = requests.get(url)

        #  Sometimes google will throw a 403
        if resp.status_code != 200:
            print("Request failed when looking up url: %s" % url)
        else:
            book.coverurl = url.replace("http", "https")
            book.save()
            print("Successfully updated books cover URL")
