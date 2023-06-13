from django.urls import path

from . import views

urlpatterns = [
    path('', views.chatbot, name='home'),
    path('login/', views.login_view, name='login')
]
