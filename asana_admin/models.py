import asana
import os
from django.db import models

TOKEN = os.environ.get('TOKEN', None)
client = asana.Client.access_token(TOKEN)
workspaces = list(client.workspaces.get_workspaces({}, opt_pretty=True))
workspaces_choices = [(w['gid'], w['name']) for w in workspaces]


if len(workspaces) == 0:
    raise Exception('No workspaces exist on account')
# Pick the first one
WORKSPACE = workspaces[0]['gid']

class User(models.Model):
    identifier = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if not self.pk:
            result =  client.workspaces.add_user_for_workspace(WORKSPACE, {
                'user': self.name
                }, opt_pretty=True)
            self.identifier = result.get('gid', None)

        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Project(models.Model):
    identifier = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if not self.pk:
            result = client.projects.create_project({
                'name': self.name, 'workspace': WORKSPACE
                }, opt_pretty=True)
            self.identifier = result.get('gid', None)
        else:
            result = client.projects.update_project(
                self.identifier, {'name': self.name}, opt_pretty=True
            )       
        
        super(Project, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Task(models.Model):
    identifier = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_text = models.CharField(max_length=1024)
    implementer = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        data = {
            'name': self.task_text,
            'assignee': self.implementer.identifier,
        }

        if not self.pk:
            data['projects'] = self.project.identifier,
            result = client.tasks.create_in_workspace(WORKSPACE, data)
            self.identifier = result.get('gid', None)
        else:
            result = client.tasks.update_task(self.identifier, data, opt_pretty=True)

        super(Task, self).save(*args, **kwargs)
