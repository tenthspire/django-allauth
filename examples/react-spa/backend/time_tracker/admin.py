from django.contrib import admin




from time_tracker.models import *


# Register your models here.

@admin.register(Project)
class ProjectAdminModel(admin.ModelAdmin):
    list_display = ("id", "user", "name", "status")
    search_fields = ('id', 'user__id')


@admin.register(Task)
class TaskAdminModel( admin.ModelAdmin):
    list_display = ("id", "user", "name", "status")
    search_fields = ('id', 'user__id')


@admin.register(AssignTask)
class AssignTaskAdminModel( admin.ModelAdmin):
    list_display = ("id", "developer", "task")
    search_fields = ('id', 'developer__id', 'task__id')


@admin.register(TimeLogTask)
class TimeLogTaskAdminModel( admin.ModelAdmin):
    list_display = ("id", "developer", "assigned_task", 'note')
    search_fields = ('id', 'developer__id', 'assign_task__id')


@admin.register(Comments)
class CommentsAdminModel( admin.ModelAdmin):
    list_display = ("id", "user", "task")
    search_fields = ("id", "user__id", "task__id")


@admin.register(TimeTracker)
class TimeTrackerAdminModel( admin.ModelAdmin):
    list_display = ("id", "user", "is_active")


@admin.register(TimeLogValidation)
class TimeLogValidationAdminModel(admin.ModelAdmin):
    list_display = ("id", "time_tracker", "created_at", "validate_at")
