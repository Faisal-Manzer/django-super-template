# pylint: disable=W0614
"""
Override base settings for development
    DEBUG: true
    PRODUCTION: false
"""


# pylint: disable=W0401
from .base import *

INSTALLED_APPS += ['example']
ALLOWED_HOSTS = ['*']
