from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Timesheet, Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)  # Datos del dueño del proyecto
    members = UserSerializer(many=True, read_only=True)  # Lista de miembros
    members_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'members', 'members_ids', 'status', 'created_at']

    def create(self, validated_data):
        members = validated_data.pop('members_ids', [])
        project = Project.objects.create(**validated_data)
        project.members.set(members)
        return project

class TimesheetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Timesheet
        fields = ['id', 'user', 'project', 'date', 'hours', 'notes', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'due_date', 'completed', 'project', 'assigned_to']
