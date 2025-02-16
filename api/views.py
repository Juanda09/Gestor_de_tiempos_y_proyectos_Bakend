from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import Project, Timesheet, Task
from .serializers import UserSerializer, ProjectSerializer, TimesheetSerializer, TaskSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(is_active=True)  # Solo proyectos activos

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Asignar dueño al proyecto

class TimesheetViewSet(viewsets.ModelViewSet):
    serializer_class = TimesheetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Timesheet.objects.filter(user=self.request.user, is_active=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Asignar usuario autenticado

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save()
