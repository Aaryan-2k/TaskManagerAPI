from django.db import models

# Create your models here.
class TaskModel(models.Model):
    title=models.CharField(max_length=250)
    description=models.TextField()
    completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
