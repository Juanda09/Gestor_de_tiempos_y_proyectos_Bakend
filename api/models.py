from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

class BaseModel(models.Model):
    """Modelo base para agregar timestamps y borrado lógico."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  # Soft delete

    class Meta:
        abstract = True


class Project(BaseModel):
    """Modelo para representar proyectos."""
    
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
    
    def add_member(self, user):
        """Agrega un miembro al proyecto."""
        self.members.add(user)

    def change_status(self, new_status):
        """Cambia el estado del proyecto."""
        if new_status in dict(self.STATUS_CHOICES):
            self.status = new_status
            self.save()

    def save(self, *args, **kwargs):
        """Lógica adicional antes de guardar."""
        if self.status == 'completed' and not hasattr(self, 'completed'):
            self.completed = True
        super().save(*args, **kwargs)


class Timesheet(BaseModel):
    """Modelo para registrar el tiempo trabajado en proyectos."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="timesheets")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="timesheets")
    date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'project', 'date')  # Evita duplicados por usuario y fecha
    
    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.date})"
    
    def clean(self):
        """Validaciones personalizadas."""
        if self.hours < 0:
            raise ValidationError("Las horas trabajadas no pueden ser negativas.")
    
    def save(self, *args, **kwargs):
        """Lógica adicional antes de guardar."""
        self.clean()  # Realizamos la validación antes de guardar
        super().save(*args, **kwargs)


class Task(BaseModel):
    """Modelo para representar tareas asignadas a proyectos."""
    
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
    
    def clean(self):
        """Validaciones personalizadas."""
        if self.due_date and self.due_date < self.created_at.date():
            raise ValidationError("La fecha de vencimiento no puede ser anterior a la fecha de creación.")
    
    def save(self, *args, **kwargs):
        """Lógica adicional antes de guardar."""
        self.clean()  # Realizamos la validación antes de guardar
        super().save(*args, **kwargs)


# Signal para enviar correo cuando una tarea es completada
@receiver(post_save, sender=Task)
def send_task_completed_email(sender, instance, created, **kwargs):
    """Envía un correo cuando una tarea es completada."""
    if instance.completed:
        send_mail(
            'Tarea Completada',
            f'La tarea "{instance.title}" ha sido completada.',
            'from@example.com',
            [instance.assigned_to.email],
            fail_silently=False,
        )
