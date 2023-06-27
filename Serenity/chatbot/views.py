from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect
from api_reader_pdf.models import *


# Create your views here.

def chatbot(request):
    if request.user.is_authenticated:
        user = request.user
        nombre_archivos = list(Embedding.objects.filter(usuario=user).values_list('nombre_archivo', flat=True))
        identificadores = list(Embedding.objects.filter(usuario=user).values_list('identificador', flat=True))
        combined_data = zip(nombre_archivos, identificadores)
        context = {'nombre_archivos': nombre_archivos, 'identificadores': identificadores, 'data': combined_data}
        return render(request, 'chatbot/index.html', context)
    else:
        return render(request, 'chatbot/index.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def ht(request):
    return render(request, 'chatbot/in.html')

@login_required
def chat_pdf(request, user_username, identificador):
    user = get_object_or_404(Usuario, username=user_username)
    nombre_archivos = list(Embedding.objects.filter(usuario=user).values_list('nombre_archivo', flat=True))
    identificadores = list(Embedding.objects.filter(usuario=user).values_list('identificador', flat=True))
    combined_data = zip(nombre_archivos, identificadores)
    context = {
    'user_username': user_username,
    'data': combined_data,
    'identificador':  identificador,
    }
    return render(request, 'chatbot/chat.html', context)

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


        