from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProjectViewSet, TimesheetViewSet, TaskViewSet, RegisterView

# Crea un enrutador para los viewsets
router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'timesheets', TimesheetViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('auth/', include('djoser.urls')),  # Rutas para gestión de usuarios
    path('auth/', include('djoser.urls.jwt')),  # JWT para autenticación
    path('register/', RegisterView.as_view()),  # Registro de usuario
]
