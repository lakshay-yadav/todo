from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null= True)
    title = models.CharField(max_length=255)
    description = models.TextField(default="Please add description",null=False)
    status = models.CharField(max_length=100,default="In Progress")
    email = models.EmailField(null=True)

    def __str__(self):
        return self.title