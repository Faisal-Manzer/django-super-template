"""Test utilities"""

__all__ = [
    'ClientTestCase', 'UserTestCase', 'with_login',
    'AdminUserTestCase', 'StaffUserTestCase'
]

import json

from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth.models import User

from encrypt import get_random_password


class ClientTestCase(TestCase):
    """Extends TestCase as DRY"""
    json_content_type = 'Content-Type'

    def setUp(self):
        """Setup client for testing"""

        self.client = Client()

    @staticmethod
    def url(*args, **kwargs):
        """Method to call for reverse, will reduce imports"""
        return reverse(*args, **kwargs)

    def assertContentType(self, response, content_type):
        """Test for specific content type"""
        self.assertEqual(response.__getitem__('Content-Type'), content_type)

    def assertJSONResponse(self, response):
        """Test JSON response and validates response as JSON"""
        self.assertContentType(response, 'application/json')
        return json.loads(response.content)

    def assertJSONResponseCode(self, response, expected_code):
        """Tests valid JSON and response_code"""
        self.assertEqual(response.status_code, expected_code)
        return self.assertJSONResponse(response)

    def assertNoAuthentication(self, response):
        """Tests is authenticated"""
        self.assertEqual(response.status_code, 401)
        json_response = self.assertJSONResponse(response)
        self.assertEqual(json_response['detail'], 'Authentication credentials were not provided.')


class UserTestCase(ClientTestCase):
    """Creates a created_by to test"""

    username = 'test-created_by'
    email = 'test@created_by.com'
    user_creator = User.objects.create_user
    extra_user_credentials = {}
    user = None

    def setUp(self):
        """Set self.created_by to newly created created_by"""

        super(UserTestCase, self).setUp()
        self.password = get_random_password(20)
        self.user = self.user_creator(
            **self.get_credentials(),
            **self.get_user_extra_creation_fields()
        )

    def get_credentials(self):
        """Get credentials for login and creation of created_by"""

        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
        }

    def get_user_extra_creation_fields(self):
        """Gives extra fields when creating created_by"""
        return self.extra_user_credentials


def with_login(func):
    """Method decorator helps in testing created_by; Login in start of test and logout at end"""

    def wrapper(self, *args, **kwargs):
        """Main Decorator"""

        self.client.login(**self.get_credentials())
        func(self, *args, **kwargs)
        self.client.logout()

    return wrapper


class AdminUserTestCase(UserTestCase):
    """Extends UserTestCase where created_by is specifically an Admin"""

    extra_user_credentials = {'is_staff': True, 'is_superuser': True}


class StaffUserTestCase(UserTestCase):
    """Extends UserTestCase where created_by is specifically a Staff User"""

    extra_user_credentials = {'is_staff': True, 'is_superuser': False}
