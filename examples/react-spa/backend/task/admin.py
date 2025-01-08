from django.contrib import admin

# Register your models here.
from task.models import Project
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "estimate_time")