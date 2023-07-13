from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager

class User(AbstractUser):
    sw_numer = models.CharField(max_length=100)
    sw_password = models.CharField(max_length=100)
    objects = UserManager()