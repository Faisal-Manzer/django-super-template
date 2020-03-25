"""WebSocket routing"""


from django.urls import path

from utils.core import ws_include


ws_urlpatterns = [
    path('example/', ws_include('example.urls')),
]
