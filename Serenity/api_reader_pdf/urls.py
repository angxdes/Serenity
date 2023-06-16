from django.urls import path
from .views import create_embeddings_url, talk_pdf
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('create_embeddings_url', login_required(create_embeddings_url), name='create-embeddings'),
    path('talk_pdf/', login_required(talk_pdf), name='talk_pdf')
]
