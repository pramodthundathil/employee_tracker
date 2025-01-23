from django.db import models

# Create your models here.
class Task(models.Model):
    employee = models.ForeignKey('home.CustomUser', on_delete=models.CASCADE, related_name='tasks')
    manager = models.ForeignKey('home.CustomUser', on_delete=models.CASCADE, related_name='assigned_tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TaskUpdate(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='updates')
    update_text = models.TextField()
    files = models.FileField(upload_to='task_files', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update for {self.task.title} at {self.created_at}"