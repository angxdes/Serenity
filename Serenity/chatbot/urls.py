from django.urls import path

from . import views

urlpatterns = [
    path('', views.chatbot, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('<str:user_username>/<str:identificador>/', views.chat_pdf, name='chat_pdf'),
]
