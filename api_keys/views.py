from django.shortcuts import render
from rest_framework import viewsets, status
from .models import APIKey
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import APIKeySerializer
from .services import APIKeyService
# Create your views here.

class APIKeyViewSet(viewsets.ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class = APIKeySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get("name")
        project = serializer.validated_data.get("project")
        

        if project.owner != self.request.user:
            return Response(
                {"error": "You do not own such project"}, status.HTTP_403_FORBIDDEN
            )

        result = APIKeyService.create_api_key(name, project, self.request.user)
        response_serializer = self.get_serializer(result["api_key_model"])
        response_data = response_serializer.data
        response_data["api_key"] = result["api_key"]

        return Response(response_data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        return APIKey.objects.filter(project__owner=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        
        api_key = self.get_object()
        api_key.is_active = False
        api_key.save(update_fields=["is_active"])

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    