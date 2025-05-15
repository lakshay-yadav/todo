from django.db import models
from django.contrib.auth.models import User


class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)


class todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null= True)
    title = models.CharField(max_length=255)
    description = models.TextField(default="Please add description",null=False)
    status = models.CharField(max_length=100,default="In Progress")

    def __str__(self):
        return self.title