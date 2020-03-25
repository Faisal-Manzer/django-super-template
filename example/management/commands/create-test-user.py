"""Adds a test superuser to allow login; change behaviour in secrets.json"""


from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from __config__.secrets import SECRET


class Command(BaseCommand):
    """Handel command"""

    def handle(self, *args, **options):
        """Adds test user for development use"""

        print('Creating default user...')
        User = get_user_model()
        user_default = SECRET['TEST_USER']

        u = User(username=user_default['USERNAME'])
        u.set_password(user_default['PASSWORD'])
        u.is_superuser = True
        u.is_staff = True
        u.save()

        print('Created...', u)
