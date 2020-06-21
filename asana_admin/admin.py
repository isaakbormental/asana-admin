from django.contrib import admin
from .models import Task, Project, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ["identifier"]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ["identifier"]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ["identifier"]