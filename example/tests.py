# pylint: disable=W0614
"""Tests for Example app"""

import json

from channels.testing import WebsocketCommunicator
from django.test import TestCase
from asgiref.sync import async_to_sync

# pylint: disable=W0401
from utils.test import *
from .models import Person
from .consumers import PingPongConsumer
from .tasks import add


class TemplateTestCase(ClientTestCase):
    """Test all template rendering"""

    def test_websocket_browser_view(self):
        """Test correct render of example:websocket-browser-test-page"""

        url = self.url('example:websocket-browser-test-page')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'example/websocket-browser-test.html')
        self.assertContains(response, 'WebSocket Test')


class PersonTestCase(StaffUserTestCase):
    """Test Person Rest APIs"""
    list_create_url_name = 'example:person-list-create'

    def setUp(self):
        """Create 2 items for different tests"""
        super(PersonTestCase, self).setUp()

        Person.objects.create(name="Name1", created_by=self.user)
        Person.objects.create(name="name2", created_by=self.user)

    def test_title_case_name(self):
        """Name should be title cased before saving"""
        name2 = Person.objects.get(name__iexact='name2')
        self.assertEqual(name2.name, 'Name2')

    def test_person_say_hello(self):
        """Should say hello to person"""

        name1 = Person.objects.get(name='Name1')
        self.assertEqual(name1.say_hello(), 'Hello Name1')

    def __request_create_person__(self, name):
        """Creates a random hello via API"""

        url = self.url(self.list_create_url_name)
        return self.client.post(url, data={
            'name': name
        })

    def test_create_no_authentication(self):
        """Try to create without authentication"""

        response = self.__request_create_person__('Unauthorized Person')
        self.assertNoAuthentication(response)

    @with_login
    def test_create(self):
        """Try creation of Person object"""

        name = 'Authorized hello'
        response = self.__request_create_person__(name)
        json_response = self.assertJSONResponseCode(response, 201)
        self.assertEqual(json_response['name'], name.title())

    @with_login
    def test_create_without_name(self):
        """Try creation without name"""

        url = self.url(self.list_create_url_name)
        response = self.client.post(url, data={})
        json_response = self.assertJSONResponseCode(response, 400)
        self.assertEqual(json_response['name'], ['This field is required.'])

    def test_list(self):
        """Test creation of a Person item"""

        count = Person.objects.all().count()
        url = self.url(self.list_create_url_name)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        json_response = self.assertJSONResponse(response)

        self.assertIsInstance(json_response['results'], list)
        assert json_response['count'] <= count


class PingPongWebSocketTestCase(TestCase):
    """Test ping pong consumer"""

    @async_to_sync
    async def test_ping_pong(self):
        """Main test"""

        communicator = WebsocketCommunicator(
            PingPongConsumer,
            '/example/test/'
        )
        connected, _ = await communicator.connect()
        assert connected
        await communicator.send_to(text_data=json.dumps({'type': 'ping'}))
        response = await communicator.receive_from()
        assert response == json.dumps({'message': 'pong'})


class BackgroundExecutionTest(TestCase):
    """Test background task"""

    def test_background_add(self):
        """Example test for adding two numbers"""

        result = add.delay(8, 8)
        x = result.get()
        self.assertEqual(x, 16)
        self.assertTrue(result.successful())
