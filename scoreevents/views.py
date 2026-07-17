from django.shortcuts import render
from .models import ScoreEvent
from .serializers import ScoreEventSerializer
from .services import ScoreEventService
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response

# Create your views here.
