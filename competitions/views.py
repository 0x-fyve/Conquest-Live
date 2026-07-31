from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Competition
from .serializers import CompetitionSerializer, LeaderboardEntrySerializer
from .services import CompetitionService
from rest_framework.decorators import action
from participants.models import Participant
from participants.serializers import ParticipantSerializer
from django.db.models import Sum
from django.db.models.functions import Coalesce
from scoreevents.serializers import ScoreEventSerializer
from scoreevents.models import ScoreEvent
from drf_spectacular.utils import extend_schema

# Create your views here.
@extend_schema(tags=["Competitions"])
class CompetitionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CompetitionSerializer

    def get_queryset(self):
        return Competition.objects.filter(project__owner=self.request.user)
        
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data.get("name")
        project = serializer.validated_data.get("project")

        if project.owner != self.request.user:
            return Response(
                {"error": "You do not own such project"}, status.HTTP_403_FORBIDDEN
            )
        description = serializer.validated_data.get("description", "")
        rules = serializer.validated_data.get("rules", None)
        starts_at = serializer.validated_data.get("starts_at", None)
        ends_at = serializer.validated_data.get("ends_at", None)
        
        competition = CompetitionService.create_competition(
            name=name,
            project=project,
            description=description,
            rules=rules,
            starts_at=starts_at,
            ends_at=ends_at,
        )
        response_serializer = self.get_serializer(competition)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=["get"])
    def leaderboard(self, request, pk=None):
        competition = self.get_object()

        if competition.project.owner != self.request.user:
            return Response(
                {"error": "You do not own this competition."},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        query = Participant.objects.filter(
            competition=competition).annotate(
            total_score=Coalesce(
                Sum("scoreevents__points"),
                0
            )).order_by("-total_score", "display_name")
        
        for index, participant in enumerate(query, start=1):
            participant.rank = index

        serializer = LeaderboardEntrySerializer(query, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def participants(self, request, pk=None):
        competition = self.get_object()

        if competition.project.owner != self.request.user:
            return Response(
                {"error": "You do not own this competition."},
                status=status.HTTP_403_FORBIDDEN,
            )

        query = Participant.objects.filter(competition=competition.id).order_by("display_name")

        serializer = ParticipantSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def scoreevents(self, request, pk=None):
        competition = self.get_object()

        if competition.project.owner != self.request.user:
            return Response(
                {"error": "You do not own this competition."},
                status=status.HTTP_403_FORBIDDEN,
            )

        query = ScoreEvent.objects.filter(competition=competition.id).order_by("-created_at")

        serializer = ScoreEventSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def summary(self, request, pk=None):
        competition = self.get_object()

        if competition.project.owner != self.request.user:
            return Response(
                {"error": "You do not own this competition."},
                status=status.HTTP_403_FORBIDDEN,
            )

        total_score = ScoreEvent.objects.filter(competition=competition.id).aggregate(
            total_score=Coalesce(Sum("points"), 0)
        )["total_score"]

        total_participants = Participant.objects.filter(competition=competition.id).count()

        first = Participant.objects.filter(competition=competition.id).annotate(
            total_score=Coalesce(Sum("scoreevents__points"), 0)
        ).order_by("-total_score", "display_name").first()

        first.rank = 1
        summary_data = {
            "total_participants": total_participants,
            "total_score": total_score,
            if first:
                "first_place": LeaderboardEntrySerializer(first).data
            "status": competition.status,
        }

        return Response(summary_data, status=status.HTTP_200_OK)

