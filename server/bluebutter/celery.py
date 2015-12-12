from __future__ import absolute_import

from celery import Celery

from django.conf import settings
import django
from server import settings as server_settings

try:
    settings.configure(
        DATABASES = server_settings.DATABASES,
        REDIS_HOST=server_settings.REDIS_HOST,
        REDIS_PORT=server_settings.REDIS_PORT,
        REDIS_COUNTS_DB=server_settings.REDIS_COUNTS_DB,
    )
except RuntimeError:
    print("It appears settings were already configured. Ignoring exception")

django.setup()

app = Celery('bluebutter',
             broker='amqp://',
             backend='amqp://',
             include=[
                'bluebutter.emailtasks',
                'bluebutter.imagetasks',
                'bluebutter.usertasks',
                'bluebutter.searchtasks',
             ])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()
