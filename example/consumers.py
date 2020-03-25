"""WebSocket consumers for Example App"""

__all__ = ['PingPongConsumer']


import json

from channels.generic.websocket import AsyncWebsocketConsumer


class PingPongConsumer(AsyncWebsocketConsumer):
    """Test WebSocket connection in browser"""

    room_group_name = 'websocket-browser-test'

    async def connect(self):
        """Accept connection to socket"""
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        """Disconnect from socket"""

        print('Disconnecting to socket...', code)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        """Receive ping and forward message to group"""

        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']

        # Check for `ping` as message
        assert message_type == 'ping'

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'pong', 'message': text_data_json}
        )

    async def pong(self, _):
        """Sends `pong` as message"""

        await self.send(text_data=json.dumps({
            'message': 'pong'
        }))
