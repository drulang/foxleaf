from __future__ import absolute_import

from bluebutter.celery import app
from cobalt import models


@app.task
def determine_scene_top_art(sceneid):
    scene = models.Scene.objects.filter(id=sceneid).first()

    if not scene:
        print("Unable to find scene with id: %s" % sceneid)

@app.task
def determine_top_art_for_scenes():
    pass
