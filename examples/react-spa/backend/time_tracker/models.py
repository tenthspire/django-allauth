import os
import uuid
from django.db import models

# Create your models here.
from users.models import CustomUser




def get_time_log_validation_path(instance, filename):
    return os.path.join('image', 'time_log_validation', '{}.{}'.format(uuid.uuid4(), filename.split('.')[-1]))


class Project(models.Model):
    Project_Status = (
        ('active', 'Active'),
        ('in-progress', 'InProgress'),
        ('completed', 'Completed')
    )

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    team = models.ManyToManyField(CustomUser, related_name='developer_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimate_time = models.FloatField(default=0)
    name = models.CharField(max_length=200, null=False, blank=True)
    description = models.TextField(null=False, blank=True)
    status = models.CharField(choices=Project_Status, max_length=20, default='active')


class Task(models.Model):
    Task_Status = (
        ('active', 'Active'),
        ('in-progress', 'InProgress'),
        ('completed', 'Completed')
    )

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=False, blank=True)
    description = models.TextField(null=False, blank=True)
    estimate_time = models.FloatField(default=0)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(choices=Task_Status, max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TODO create total time sum of AssignTask


class AssignTask(models.Model):
    developer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TODO create total time sum of TimeLogTask


class TimeLogTask(models.Model):
    developer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=False, default=None)
    end_time = models.DateTimeField(null=False, default=None)
    total_time_hr = models.CharField(max_length=200, null=True, blank=True)
    assigned_task = models.ForeignKey(AssignTask, on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comments(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.TextField(null=True, blank=True, default=None)


class TimeTracker(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)


class TimeLogValidation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    time_tracker = models.ForeignKey(TimeTracker, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to=get_time_log_validation_path, help_text='Validation Image', blank=True,
                              null=True)
    validate_at = models.DateTimeField(auto_now_add=True)
