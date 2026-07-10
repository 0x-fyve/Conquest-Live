from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Competition
from .serializers import CompetitionSerializer
from .services import CompetitionService
# Create your views here.

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
