from django.shortcuts import render

# Create your views here.

def chatbot(request):
    return render(request, 'chatbot/index.html')

def login_view(request):
    return render(request, 'chatbot/sign-in.html')