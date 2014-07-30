from __future__ import absolute_import

import os

from celery import Celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'southwest.settings')  # todo is this correct?

app = Celery('sw_checkin')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Configure celery to use the django-celery backend
app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_ENABLE_UTC=True
    # CELERY_TIMEZONE='America/Los_Angeles'
)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))