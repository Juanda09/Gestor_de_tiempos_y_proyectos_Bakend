from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    """Modelo base para agregar timestamps y borrado lógico."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  # Soft delete

    class Meta:
        abstract = True

class Project(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('completed', 'Completado'),
        ('archived', 'Archivado'),
    ]

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_projects")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    members = models.ManyToManyField(User, related_name="projects")  # Relación de equipo

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"

class Timesheet(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="timesheets")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="timesheets")
    date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'project', 'date')  # Evita duplicados por usuario y fecha

    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.date})"

class Task(BaseModel):
    """Nueva entidad para asignar tareas a proyectos."""
    PRIORITY_CHOICES = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.get_priority_display()})"
