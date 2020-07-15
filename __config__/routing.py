"""Overrides wsgi server for websocket control"""


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from __config__.urls import websocket


APPLICATION = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket.ws_urlpatterns
        )
    ),
})
