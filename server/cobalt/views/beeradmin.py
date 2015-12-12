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


def bookadmin(request):
    if not request.user.is_authenticated():
        return redirect('/')
    elif not request.user.is_superuser:
        return redirect('/')

    books = models.Book.objects.all()

    columns = divide_into_columns(4, books)

    context = {
        "col_1": columns[0],
        "col_2": columns[1],
        "col_3": columns[2],
        "col_4": columns[3],
        'books': books,
    }

    return render(request, 'cobalt/bookadmin.html', context)
