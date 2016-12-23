from django.db import models

# Create your models here.

class UserInfo(models.Model):
    name = models.CharField(max_length=30,null=True)
    phone = models.CharField(max_length=30,null=True)
    pwd = models.CharField(max_length=30)
