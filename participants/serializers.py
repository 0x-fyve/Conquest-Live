from rest_framework import serializers
from .models import Participant

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = (
            "id",
            "competition",
            "external_id",
            "display_name",
            "metadata",
            "is_active",
            "joined_at",
        )
        read_only_fields = (
            "id",
            "joined_at",
        )
