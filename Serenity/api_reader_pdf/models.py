from django.db import models
from chatbot.models import Usuario

class Embedding(models.Model):
    contenido_texto = models.JSONField()
    embeddings = models.JSONField()
    nombre_archivo = models.CharField(max_length=100, default="S/N")
    identificador = models.CharField(max_length=30, default='00000000000000000000')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='embeddings', null=True)

    def __str__(self):
        return self.usuario
