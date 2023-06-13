from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import *
from .utils import *
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required

used_sessions = set()

@ensure_csrf_cookie
@require_POST
@transaction.atomic
def create_embeddings_url(request):
    csrf_token = request.COOKIES.get('csrftoken')
    print(f"CSRF Token: {csrf_token}")
    url = request.POST.get("url")
    nombre_archivo = request.POST.get("nombre_archivo")

    if request.user.is_authenticated:
        try:
            Embedding.objects.get(nombre_archivo=nombre_archivo)
            return JsonResponse({"message": "Un archivo con ese nombre ya existe"})
        except Embedding.DoesNotExist:
            pdf_text = pdf_to_text(url)
            pdf_dfs(nombre_archivo, pdf_text)
            return JsonResponse({"message": "Embeddings created successfully."})
    else:
        # El usuario no está registrado, verificar si ya se ha utilizado el endpoint
        session_key = request.session.session_key
        if session_key is None or not UsedSession.objects.filter(session_key=session_key).exists():
            UsedSession.objects.create(session_key=session_key)
            try:
                Embedding.objects.get(nombre_archivo=nombre_archivo)
                return JsonResponse({"message": "Un archivo con ese nombre ya existe"})
            except Embedding.DoesNotExist:
                pdf_text = pdf_to_text(url)
                pdf_dfs(nombre_archivo, pdf_text)
                return JsonResponse({"message": "Embeddings created successfully."})
        else:
            return JsonResponse({"message": "No tienes permitido utilizar el endpoint nuevamente."})
