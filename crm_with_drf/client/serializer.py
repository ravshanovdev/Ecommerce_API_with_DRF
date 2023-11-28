from rest_framework import serializers
from .models import Client, Note

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email'

        ]


class ClientSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Client

        fields = [
            'id',
            'team',
            'name',
            'contact_person',
            'email',
            'web_site',
            'created_by',
            'created_at'
        ]


class NoteSerializer(serializers.ModelSerializer):
    read_only = (
        'client_id',
        'created_by'
    )

    class Meta:
        model = Note
        fields = ['id', 'name', 'body', 'created_by', "client_id"]


