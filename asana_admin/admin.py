from django.contrib import admin
from .models import Task, Project, User, WORKSPACE, workspaces_choices
from django import forms
from . import models


class ProjectForm(forms.ModelForm):
    workspaces = forms.ChoiceField(
    	choices = workspaces_choices,
    	label="",
    	initial='',
    	widget=forms.Select(),
    	required=True,
    )

    class Meta:
        model = Project
        fields = '__all__'

    def save(self, *args, **kwargs):
        models.WORKSPACE = self.data.get('workspaces')
        return super(ProjectForm, self).save(*args, **kwargs)




@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ["identifier"]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ["identifier"]
    form = ProjectForm
    

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ["identifier"]