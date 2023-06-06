from django.db import models
from django.contrib.auth.models import AbstractUser


class Embedding(models.Model):
    nombre_archivo = models.CharField(max_length=255)
    contenido_texto = models.JSONField()
    embeddings = models.JSONField()

    def __str__(self):
        return self.nombre_archivo

class Usuario(AbstractUser):
    embedding = models.ForeignKey(Embedding, on_delete=models.SET_NULL, null=True)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username