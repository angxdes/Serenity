from django.urls import path
from .views import create_embeddings_url

urlpatterns = [
    path('create_embeddings_url', create_embeddings_url, name='create-embeddings'),
]
