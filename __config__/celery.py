"""Default celery task settings"""

import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '__config__.settings')
WORKER = Celery('config')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
WORKER.config_from_object('django.conf:settings')
WORKER.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@WORKER.task(bind=True)
def debug_task(self):
    """Just a test task which prints request"""

    print('Request: {0!r}'.format(self.request))
