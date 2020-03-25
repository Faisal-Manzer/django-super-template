"""Background task for Example app"""
from __config__.celery import WORKER


@WORKER.task()
def add(x, y):
    """Adds two number"""
    return x + y
