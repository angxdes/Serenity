from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import *
from .utils import *
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.sessions.models import Session
from django.db import transaction
from django.contrib.auth.decorators import login_required

used_sessions = set()

@ensure_csrf_cookie
@require_POST
@ensure_csrf_cookie
@transaction.atomic
def create_embeddings_url(request):
    csrf_token = request.COOKIES.get('csrftoken')
    print(f"CSRF Token: {csrf_token}")

    url = request.POST.get("url")

    if not url:
        return JsonResponse({"message": "Invalid data."}, status=400)
    
    # Acceder al usuario autenticado
    user = request.user
    if user.is_authenticated:
        user_username = user.username
        user_id = user.id    
        nombre_archivo, pdf_text  = pdf_to_text(url)
        pdf_dfs(user_id, pdf_text, nombre_archivo)

        # Obtener el último embedding creado para el usuario
        embedding = Embedding.objects.filter(usuario=user).latest('id')

        return JsonResponse({"message": "Embeddings created successfully.", "embedding_id": embedding.identificador})

    return JsonResponse({"message": "Authentication required."}, status=401)


@login_required
@require_POST
def talk_pdf(request):
    identificador = request.POST.get('identificador')
    question = request.POST.get('question')
    model="text-davinci-003"
    answer = answer_question(identificador,model, question)

    return JsonResponse({'answer': answer}) 



