from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProjectViewSet, TimesheetViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'timesheets', TimesheetViewSet, basename='timesheets')
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('api/', include(router.urls)),
    path('auth/', include('djoser.urls')),  # Rutas para gestión de usuarios
    path('auth/', include('djoser.urls.jwt')),  # JWT para autenticación
]
