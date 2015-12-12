from __future__ import absolute_import

from bluebutter.celery import app
from cobalt import models
from django.db import connection

@app.task
def add_point_to_user(userid, point_code):
    point = models.Point.objects.filter(code=point_code).first()
    if point:
        userpoint= models.UserPoint(user_id=userid, point=point).save()
        calculate_user_points(userid)

@app.task
def calculate_user_points(userid):
    user =  models.User.objects.filter(id=userid).first()
    if not user:
        print("Unable to find uesr with id: %s" % userid)
        return
 
    print("Updating points for user: %s" % userid)

    cursor = connection.cursor()
    query = 'select sum(value) from cobalt_userpoint up inner join cobalt_point p on up.point_id = p.id where up.user_id = %d;' % userid
    cursor.execute(query)

    row = cursor.fetchone()
    user.currpoint = row[0]
    user.save()
