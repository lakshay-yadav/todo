from django.db import models

# Create your models here.
class todo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(default="In progress")

    def __str__(self):
        return self.title