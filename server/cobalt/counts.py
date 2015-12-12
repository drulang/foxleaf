import redis

from django.conf import settings


BOOK_COUNT_KEY  = "viewcount:bookid:%s"
SCENE_COUNT_KEY = "viewcount:sceneid:%s"
ART_COUNT_KEY   = "viewcount:artid:%s"

redis_counts_conn = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_COUNTS_DB)

def increment_view_count_for_art_id(art_id):
    if not art_id:
        raise ValueError("art_id cannot be null or empty")

    key = ART_COUNT_KEY % art_id
    redis_counts_conn.incr(key)

def increment_view_count_for_scene_id(scene_id):
    if not scene_id:
        raise ValueError("scene_id cannot be null or empty")
    key = SCENE_COUNT_KEY % scene_id
    redis_counts_conn.incr(key)

def increment_view_count_for_book_id(book_id):
    if not book_id:
        raise ValueError("book_id cannot be null or empty")
    key = BOOK_COUNT_KEY % book_id
    redis_counts_conn.incr(key)

def view_count_for_book_id(book_id):
    if not book_id:
        raise ValueError("book_id cannot be null or empty")
    key = BOOK_COUNT_KEY % book_id
    return redis_counts_conn.get(key)

def view_count_for_scene_id(scene_id):
    if not scene_id:
        raise ValueError("scene_id cannot be null or empty")
    key = SCENE_COUNT_KEY % scene_id
    return redis_counts_conn.get(key)

def view_count_for_art_id(art_id):
    if not art_id:
        raise ValueError("art_id cannot be null or empty")
    key = ART_COUNT_KEY % art_id
    return redis_counts_conn.get(key)
