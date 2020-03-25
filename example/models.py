"""Models for Example app"""


from django.db import models

from django_lifecycle import LifecycleModel, hook


class Person(LifecycleModel):
    """Test models; saves name and say hello"""

    name = models.CharField(max_length=255)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @hook('before_save')
    def capitalize_name(self):
        """Title case name"""

        self.name = self.name.title()

    def say_hello(self):
        """Say hello to person"""

        return f'Hello {self.name}'
