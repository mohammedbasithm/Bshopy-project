from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class otp_generation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    secret = models.CharField(max_length=100)
    tokens = models.CharField(max_length=10)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)