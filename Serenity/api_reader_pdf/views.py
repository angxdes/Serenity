from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import *
from .utils import *
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.db import transaction

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
        user_id = user.id    
        pdf_text = pdf_to_text(url)
        pdf_dfs(user_id, pdf_text)
        return JsonResponse({"message": "Embeddings created successfully."})

    return JsonResponse({"message": "Authentication required."}, status=401)
