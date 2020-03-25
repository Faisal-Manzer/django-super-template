"""URL routing for Example App"""

from django.urls import path
from . import views, consumers

urlpatterns = [
    path('ws-browser-test/', views.websocket_browser_test_view, name='websocket-browser-test-page'),

    path('hello/<int:pk>/',
         views.PersonRetrieveUpdateDestroyAPIView.as_view(),
         name='person-retrieve-update'),
    path('hello/', views.PersonListCreateAPIView.as_view(), name='person-list-create'),
]

ws_urlpatterns = [
    path('test/', consumers.PingPongConsumer, name='websocket-browser-test')
]

app_name = 'example'
