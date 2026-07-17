from rest_framework import serializers
from .models import ScoreEvent

class ScoreEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreEvent
        fields = (
            "id",
            "event_id",
            "competition",
            "participant",
            "points",
            "reason",
            "metadata",
            "created_at"
        )

        read_only_fields = (
            "id",
            "created_at"
        )