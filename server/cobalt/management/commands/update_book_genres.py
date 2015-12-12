import os
import time

from django.core.management.base import BaseCommand
from cobalt import models
import requests
from bs4 import BeautifulSoup 

WIKI_BASE_URL = "https://en.wikipedia.org"
SEARCH_URL = "https://en.wikipedia.org/w/index.php?search=%s"

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Updating Books")
        books = models.Book.objects.all()

        for book in books:
            print("Processing: %s" % book.title)
            query = "%s novel %s" % (book.title, book.author)
            print ("  query: %s" % query)
    
            resp = requests.get(SEARCH_URL% query)
            doc = BeautifulSoup(resp.text)
            if not doc:
                print("  No Doc")
                continue
            ele = doc.find("div", {"class": "mw-search-result-heading"})
            if not ele:
                print("  No link for book")
                continue
            link = ele.find("a").get('href')

            if not link:
                print("  Book Search Results has no url. Book: %s" % book.title)
                continue

            link = WIKI_BASE_URL + link

            time.sleep(1)            

            resp = requests.get(link)
            if resp.status_code == 200:
                print("  Was able to get wiki entry")
                doc = BeautifulSoup(resp.text)
                genre_th = doc.find(text='Genre')
                if genre_th:
                    genre_tds = genre_th.parent.parent.find("td")
                    if genre_tds:
                        genres_a = genre_tds.findAll("a")
                        genres = [genre.text.lower() for genre in genres_a]

                        # Easy thing to do right now is just clear all book genres
                        for genre in genres:
                            db_genre = models.Genre.objects.filter(name=genre).first()

                            if not db_genre:
                                db_genre = models.Genre()
                                db_genre.name = genre
                                db_genre.save()
                            
                            book.genres.add(db_genre)
                            book.save()
                else:
                    print("  No genres for book")

            time.sleep(1)

        print("~~~~~~~~~~~~~~~~~~~")
        print("Done")
        print("~~~~~~~~~~~~~~~~~~~")
