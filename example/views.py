"""Views for Example app only contains views for templates"""

__all__ = [
    'websocket_browser_test_view',
    'PersonListCreateAPIView',
    'PersonRetrieveUpdateDestroyAPIView'
]

from django.shortcuts import render

from rest_framework import generics

from .serializers import PersonSerializer
from .models import Person


def websocket_browser_test_view(request):
    """View for testing websocket with template"""

    return render(request, 'example/websocket-browser-test.html')


class PersonListCreateAPIView(generics.ListCreateAPIView):
    """Handles Person's creation and listing"""

    serializer_class = PersonSerializer
    queryset = Person.objects.all()

    def perform_create(self, serializer):
        """Add Authorised created_by to model"""
        serializer.save(created_by=self.request.user)


class PersonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Handles Person's update, destruction, and retrieval"""
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
