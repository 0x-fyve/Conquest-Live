from rest_framework import serializers
from .models import APIKey

class APIKeySerializer(serializers.ModelSerializer):

    class Meta:
        model = APIKey
        fields = (
            "id",
            "project",
            "name",
            "prefix",
            "is_active",
            "last_used_at",
            "created_by",
            "created_at",
            "expires_at",
        )
        read_only_fields = (
            "id",
            "prefix",
            "is_active",
            "last_used_at",
            "created_by",
            "created_at",
        )