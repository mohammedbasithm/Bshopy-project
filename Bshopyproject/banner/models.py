from django.db import models

# Create your models here.
class Banner(models.Model):
    name=models.CharField(max_length=200,null=True,blank=True)
    is_active=models.BooleanField(default=True)
    banner_image=models.ImageField(upload_to='Banner')
