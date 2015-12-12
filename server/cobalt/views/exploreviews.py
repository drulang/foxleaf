import json
import os
from random import shuffle, randint

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template import RequestContext, loader
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from cobalt import models
from cobalt.util import err_resp, OK, group_into_groups_of, divide_into_columns
from bluebutter import searchtasks

def search(request):
    q = request.GET.get("q", "").strip()
    books = list(models.Book.objects.search(q).all())

    char_art = models.Art.objects.search(q).filter(scene__scenetype__scenetypcd="char")
    map_art = models.Art.objects.search(q).filter(scene__scenetype__scenetypcd="map")

    books.extend(char_art.all())
    books.extend(char_art.all())

    columns = divide_into_columns(4, books)

    # Kick off a task to search google for books and index
    if q:
        searchtasks.search_google_with_query.delay(q)

    context = {
        "col_1": columns[0],
        "col_2": columns[1],
        "col_3": columns[2],
        "col_4": columns[3],
    }
    return render(request, 'cobalt/search.html', context)

def explorebooks(request, genre_name=None):
    if genre_name:
        genre = models.Genre.objects.filter(name=genre_name).first()
        if genre:
            genre_exists = True
        else:
            genre_exists = False
    else:
        # Set to True if genre_name is empty or null because this indicates
        # we're on the .../explore/books page
        genre_exists = True
        genre = None
       
    if genre_name:
        books = models.Book.objects.filter(genres__name=genre_name)
    else:
        books = models.Book.front_page

    all_media = list(books.all())
    shuffle(all_media)

    columns = divide_into_columns(4, all_media)

    context = {
        "col_1": columns[0],
        "col_2": columns[1],
        "col_3": columns[2],
        "col_4": columns[3],
        "no_primary_content": len(columns[0]) == 0,
        "genre_exists": genre_exists,
        "genre": genre,
    }

    # Find genres that users can explore
    genres = models.Genre.objects.filter(image_url__isnull=False).all()
    context['genres'] = genres

    return render(request, 'cobalt/explorebooks.html', context)

def explorescenes(request):
    all_media = list(models.Scene.objects.all())
    shuffle(all_media)

    columns = divide_into_columns(4, all_media)

    context = {
        "col_1": columns[0],
        "col_2": columns[1],
        "col_3": columns[2],
        "col_4": columns[3],
    }
    return render(request, 'cobalt/explorescenes.html', context)

def exploreart(request):
    all_media = list(models.Art.objects.all())
    shuffle(all_media)

    columns = divide_into_columns(4, all_media)

    context = {
        "col_1": columns[0],
        "col_2": columns[1],
        "col_3": columns[2],
        "col_4": columns[3],
    }
    return render(request, 'cobalt/exploreart.html', context)

