from django.shortcuts import render
from .models import ScoreEvent
from .serializers import ScoreEventSerializer
from .services import ScoreEventService
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response

# Create your views here.
class ScoreEventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ScoreEventSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        event_id = serializer.validated_data.get("event_id")
        competition = serializer.validated_data.get("competition")
        if competition.project.owner != self.request.user:
            return Response(
                {"error": "You do not own this competition."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if participant.competition != competition:
            return Response(
                {"error": "Participant does not belong to this competition."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        participant = serializer.validated_data.get("participant")


        points = serializer.validated_data.get("points")
        reason = serializer.validated_data.get("reason", "")
        metadata = serializer.validated_data.get("metadata", None)

        score_event = ScoreEventService.record_score(
            event_id=event_id,
            competition=competition,
            participant=participant,
            points=points,
            reason=reason,
            metadata=metadata
        )
        response_serializer = self.get_serializer(score_event)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        return ScoreEvent.objects.filter(
            competition__project__owner=self.request.user
        )

        
        