import os

from django.core.management.base import BaseCommand
from cobalt import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        ##
        # Book
        ##
        print("Checking Books")
        books = models.Book.objects.all()

        for book in books:
            if book.title_url and "https" not in book.coverurl[0:5]:
                print("Orig: %s" % book.coverurl)
                book.coverurl= book.coverurl.replace("http", "https")
                book.save()
        ##
        # Deviant Art
        ##
        print("Checking Art")
        arts = models.Art.objects.all()

        for art in arts:
            if art.devart_url and "https" not in art.devart_url[0:5]:
                art.devart_url = art.devart_url.replace("http", "https")
                art.save()

        print("Done")
