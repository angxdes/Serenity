from django.urls import path
from .views import create_embeddings_url
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('create_embeddings_url', login_required(create_embeddings_url), name='create-embeddings'),
]
