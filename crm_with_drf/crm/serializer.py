from rest_framework import serializers
from .models import CrmModel
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


class CrmModelSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = CrmModel

        fields = [
            'id',
            "team",
            'company',
            'contact_person',
            'email',
            'web_site',
            'confidence',
            'estimated_value',
            'status',
            'priority',
            'assigned_to',
            'created_by',
            'created_at'
        ]



