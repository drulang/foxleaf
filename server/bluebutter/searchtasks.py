from __future__ import absolute_import

from bluebutter.celery import app
from cobalt import search
from cobalt import models

@app.task
def search_google_with_query(query):
    """
    Kind of a hacky work around to index books.
    """
    print("Searching google and indexing: %s" % query)
    search.booksearch(query)

