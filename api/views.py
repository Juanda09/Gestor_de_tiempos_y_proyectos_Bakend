from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

from rest_framework import viewsets, permissions

from api.models import Project, Task, Timesheet

from .serializers import UserSerializer, ProjectSerializer, TimesheetSerializer, TaskSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class RegisterView(APIView):
    """
    Vista para el registro de usuarios.
    """
    def post(self, request, *args, **kwargs):
        # Obtén los datos del request
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        
        # Verificar si ya existe un usuario con el mismo correo
        if User.objects.filter(email=email).exists():
            return Response({"detail": "El correo electrónico ya está registrado."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Crear un nuevo usuario
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Serializar y devolver el usuario creado
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Project.objects.filter(is_active=True)  # Definir el queryset explícitamente

    def get_queryset(self):
        return Project.objects.filter(is_active=True)  # Solo proyectos activos

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Asignar dueño al proyecto

class TimesheetViewSet(viewsets.ModelViewSet):
    serializer_class = TimesheetSerializer
    permission_classes = [permissions.IsAuthenticated]

    queryset = Timesheet.objects.filter(is_active=True)  # Define el queryset explícitamente

    def get_queryset(self):
        # Aunque ya estamos definiendo un queryset explícitamente, si quieres filtrar por el usuario, usa esto:
        return Timesheet.objects.filter(user=self.request.user, is_active=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Asignar usuario autenticado
        

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Define el queryset aquí
    queryset = Task.objects.filter(is_active=True)
    
    def get_queryset(self):
        return Task.objects.filter(is_active=True)
    
    def perform_create(self, serializer):
        serializer.save()


