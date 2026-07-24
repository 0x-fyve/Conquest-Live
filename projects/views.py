from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Project
from .serializers import ProjectSerializer
from .services import ProjectService
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from competitions.models import Competition
from competitions.serializers import CompetitionSerializer

# Create your views here.


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

        
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data["name"]
        description = serializer.validated_data.get("description", "")
    
        project = ProjectService.create_project(self.request.user, name, description)
        response_serializer = self.get_serializer(project)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED,)

    @action(detail=True, methods=["get"])
    def competitions(self, request, pk=None):
        project = self.get_object()

        if project.owner != self.request.user:
            return Response(
                {"error": "You do not own this project."},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        project = self.get_object()

        query = Competition.objects.filter(project=project.id).order_by("-created_at")

        serializer = CompetitionSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

