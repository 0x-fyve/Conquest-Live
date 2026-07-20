from rest_framework import serializers
from .models import Competition

class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = (
            "id",
            "project",
            "name",
            "slug",
            "description",
            "status",
            "rules",
            "starts_at",
            "ends_at",
            "created_at",
            "updated_at"
        )

        read_only_fields= (
            "id",
            "slug",
            "status",
            "created_at",
            "updated_at"
        )

class LeaderboardEntrySerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    participant_id = serializers.UUIDField(source="id")
    display_name = serializers.CharField()
    total_score = serializers.IntegerField()
          