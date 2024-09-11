from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=10, unique=True)
    bio = models.TextField(null=True,blank=True)