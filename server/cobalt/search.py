import requests

from cobalt.models import Book
from cobalt.util import string_to_url
from bluebutter import imagetasks

VALID_CATEGORIES = [
    "fiction",
]

BASE_URL = "https://www.googleapis.com/books/v1/volumes?maxResults=40&printType=books&q=%s"

def booksearch(query):
    if not query:
        raise ValueError("Query cannot be null or empty")
    url = BASE_URL % query
    print("Request: %s" % url)

    resp = requests.get(url)
    resp = resp.json()

    book_results = []
    for book_dict in resp['items']:
        volume_info = book_dict['volumeInfo']
        # Check to see if the book is part of VALID_CATEGORIES
        is_valid = False
        for category in volume_info.get('categories',[]):
            for valid_category in VALID_CATEGORIES:
                if valid_category in category.lower():
                    is_valid = True
                    break

            if is_valid:
                break

        if not is_valid:
            continue

        # Make sure ISBN doesn't exist in db already
        isbn = None
        for ident in volume_info['industryIdentifiers']:
            if ident['type'] == "ISBN_13":
                isbn = ident['identifier']
                break

        if not isbn:
            print("Unable to create book. No ISBN_13. Title:'%s' Identifiers:%s" % (volume_info.get("title"), volume_info.get("industryIdentifiers")))
            continue

        if Book.objects.filter(isbn=isbn).exists():
            book = Book.objects.filter(isbn=isbn).first()
        else:
            try:
                book = Book()
                book.isbn = isbn
                book.title = volume_info['title']
                book.author = volume_info['authors'][0]
                book.summary = volume_info.get('description')
                book.title_url = string_to_url(book.title)
                book.publisher = volume_info.get('publisher')
                book.coverurl = volume_info['imageLinks']['thumbnail']
                book.coverurl.replace("http", "https")
                book.blessed = False
                book.save()
            except Exception as e:
                print("Unable to save book. Error: %s" % e)
                print("Volume: %s" % volume_info)

            imagetasks.adjust_book_cover_url.delay(book.id)

        book_results.append(book)

    return book_results
