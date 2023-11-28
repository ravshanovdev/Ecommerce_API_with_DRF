from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Team, Plans


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


class PlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plans
        fields = [
            "id",
            "name",
            "max_crm_models",
            "max_clients",
            "price"
        ]


class TeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    plans = PlansSerializer(read_only=True)

    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'members',
            "plans",
            'created_by',
            'created_at',

        ]




