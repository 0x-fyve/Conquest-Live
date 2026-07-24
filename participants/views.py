from django.shortcuts import render
from .models import Participant
from .serializers import ParticipantSerializer
from .services import ParticipantService
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from scoreevents.serializers import ScoreEventSerializer
from scoreevents.models import ScoreEvent

# Create your views here.
class ParticipantViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ParticipantSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        competition = serializer.validated_data.get("competition")
        if competition.project.owner != self.request.user:
            return Response(
                {"error": "You do not own this competition."},
                status=status.HTTP_403_FORBIDDEN,
            )

        external_id = serializer.validated_data.get("external_id")
        display_name = serializer.validated_data.get("display_name")
        metadata = serializer.validated_data.get("metadata", None)        

        participant = ParticipantService.create_or_update_participant(
            competition=competition,
            external_id=external_id,
            display_name=display_name,
            metadata=metadata,
        )
        response_serializer = self.get_serializer(participant)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        return Participant.objects.filter(competition__project__owner=self.request.user)

    @action(detail=True, methods=["get"])
    def scoreevents(self, request, pk=None):
        participant = self.get_object()

        if participant.competition.project.owner != self.request.user:
            return Response(
                {"error": "You do not own this participant."},
                status=status.HTTP_403_FORBIDDEN,
            )

        query = ScoreEvent.objects.filter(participant=participant.id).order_by("-created_at")

        serializer = ScoreEventSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)