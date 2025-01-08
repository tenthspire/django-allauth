from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Project
from .serializers import TaskProjectSerializer
from rest_framework.permissions import IsAuthenticated
# Create view for Task
class TaskCreate(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = TaskProjectSerializer
    permission_classes = [IsAuthenticated]

# List view for Task
class TaskList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = TaskProjectSerializer
    permission_classes = [IsAuthenticated]

# Get Task details
class TaskGetDetails(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = TaskProjectSerializer
    permission_classes = [IsAuthenticated]

# Update Task
class TaskUpdate(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = TaskProjectSerializer
    permission_classes = [IsAuthenticated]

# Delete Task
class TaskDelete(generics.DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = TaskProjectSerializer
    permission_classes = [IsAuthenticated]
