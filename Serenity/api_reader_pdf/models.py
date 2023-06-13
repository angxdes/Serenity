from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    identificacion_unica = models.CharField(max_length=255, unique=True, null=True)

class Embedding(models.Model):
    nombre_archivo = models.CharField(max_length=255)
    contenido_texto = models.JSONField()
    embeddings = models.JSONField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='embeddings', null=True)

    def __str__(self):
        return self.nombre_archivo
