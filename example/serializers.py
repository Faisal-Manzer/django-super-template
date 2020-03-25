"""Serializers for Example App"""

__all__ = ['PersonSerializer']


from rest_framework import serializers

from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    """Handles all Person model serialization for GET, PUT"""

    class Meta:
        """Meta"""
        model = Person
        fields = '__all__'
        read_only_fields = ('created_by', )
