from rest_framework import serializers
from .models import Project
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "created_at",
            "updated_at",
        )
        read_only_fields =(
            "id",
            "slug",
            "created_at",
            "updated_at"
        )