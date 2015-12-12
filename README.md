# FoxLeaf
This was an idea I had while reading The English Girl.  I was having trouble imagining what the main character looked like and thought it would be cool if there was a site to see fanart for particular characters, locations, and scenes from a book.

It's really easy to find art for popular books, but not for smaller books.  The art you do find for books is usually on sites like Deviantart which focuses on any kind of art you can imagine.  FoxLeaf is just for book related art with a focus of organizing it by the book, scene, location, and/or character.

# Stack

* Django
* Bootstrap/jQuery
* Celery with RabbitMQ
  * async tasks for image handling, Google Book API searching and local indexing, email tasks, and random tasks such as calculating user points
* GraphicsMagick
  * Image Resizing and Conversion
* PostgreSQL
* PostgreSQL Extensions - Full Text Search
* Redis
  * Counters for various page views. In the future will use the key expiration to rate limit users, chat system, other things

# Screenshots

![Homepage](https://raw.githubusercontent.com/drulang/foxleaf/master/screenshots/Screen%20Shot%202015-09-29%20at%2012.37.08%20PM.png)
![](https://github.com/drulang/foxleaf/blob/master/screenshots/Screen%20Shot%202015-09-30%20at%207.38.26%20PM.png)
![](https://github.com/drulang/foxleaf/blob/master/screenshots/Screen%20Shot%202015-09-30%20at%207.42.55%20PM.png)
![](https://github.com/drulang/foxleaf/blob/master/screenshots/Screen%20Shot%202015-09-30%20at%207.46.00%20PM.png)
![](https://github.com/drulang/foxleaf/blob/master/screenshots/Screen%20Shot%202015-09-30%20at%207.46.24%20PM.png)
![](https://github.com/drulang/foxleaf/blob/master/screenshots/Screen%20Shot%202015-09-30%20at%207.46.54%20PM.png)
![](https://github.com/drulang/foxleaf/blob/master/screenshots/Screen%20Shot%202015-09-30%20at%207.47.12%20PM.png)
![](https://github.com/drulang/foxleaf/blob/master/screenshots/Screen%20Shot%202015-09-30%20at%207.48.23%20PM.png)
![](https://github.com/drulang/foxleaf/blob/master/screenshots/Screen%20Shot%202015-09-30%20at%207.50.40%20PM.png)
![](https://github.com/drulang/foxleaf/blob/master/screenshots/Screen%20Shot%202015-09-30%20at%207.51.24%20PM.png)
![](https://github.com/drulang/foxleaf/blob/master/screenshots/Screen%20Shot%202015-09-30%20at%208.22.00%20PM.png)
![](https://github.com/drulang/foxleaf/blob/master/screenshots/Screen%20Shot%202015-09-30%20at%208.22.53%20PM.png)
![](https://github.com/drulang/foxleaf/blob/master/screenshots/Screen%20Shot%202015-09-30%20at%208.23.06%20PM.png)
![](https://github.com/drulang/foxleaf/blob/master/screenshots/Screen%20Shot%202015-09-30%20at%208.23.49%20PM.png)
![](https://github.com/drulang/foxleaf/blob/master/screenshots/Screen%20Shot%202015-09-30%20at%208.24.38%20PM.png)
