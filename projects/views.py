from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Project
from .serializers import ProjectSerializer
from .services import ProjectService
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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

