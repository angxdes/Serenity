from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    identificacion_unica = models.CharField(max_length=255, unique=True, null=True)