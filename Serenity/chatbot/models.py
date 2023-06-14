from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    company = models.CharField(max_length=20, null=True)
    def __str__(self):
        return self.email