from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect


# Create your views here.

def chatbot(request):
    return render(request, 'chatbot/index.html')

@csrf_protect
@ensure_csrf_cookie
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # Intenta autenticar al usuario por correo electrónico y contraseña
        user = Usuario.objects.filter(email=email).first()
        if user is not None and user.check_password(password):
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('home')
        
        messages.error(request, 'Invalid credentials, try again.')
        return redirect('login')
    
    return render(request, 'chatbot/sign-in.html')


@csrf_protect
@ensure_csrf_cookie
def register_view(request):
    csrf_token = request.COOKIES.get('csrftoken')
    print(f"CSRF Token: {csrf_token}")
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username'] 
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password1']
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'The Username alredy exists')
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'The email alredy exists')
        # Realizar las acciones necesarias para registrar al usuario
        # Crea una instancia de Usuarios y guarda los datos
        user = Usuario(username=username, first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save()
        messages.success(request, 'You have been register! Login in your new account.')
        return redirect('login')
    return render(request, 'chatbot/register.html')

        