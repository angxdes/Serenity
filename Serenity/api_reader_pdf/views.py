from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import *
from .utils import *
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.sessions.models import Session
from django.db import transaction
from django.contrib.auth.decorators import login_required

used_sessions = set()

@require_POST
@ensure_csrf_cookie
@transaction.atomic
def create_embeddings_url(request):
    csrf_token = request.COOKIES.get('csrftoken')
    print(f"CSRF Token: {csrf_token}")

    url = request.POST.get("url")
    file = request.FILES.get("file")

    if url == None and file == None:
        return JsonResponse({"message": "Invalid data."}, status=400)
    
    # Acceder al usuario autenticado
    user = request.user
    if user.is_authenticated:
        user_id = user.id
        if url != "":
            try:
                nombre_archivo, pdf_text  = pdf_to_text(url)
                if pdf_text == None:
                    return JsonResponse({"message": "URL no válida."})
            except:
                return JsonResponse({"message": "Error al procesar texto de la url"})
        else:
            try:
                pdf_text = pdf_doc_to_text(file)
                nombre_archivo = file.name
            except:
                return JsonResponse({"message": "Error al procesar texto del archivo"})
        try:
            pdf_dfs(user_id, pdf_text, nombre_archivo)
        except:
            return JsonResponse({"message":"Hubo un error al crear los embeddings y/o almacenarlos"})

        # Obtener el último embedding creado para el usuario
        embedding = Embedding.objects.filter(usuario=user).latest('id')

        

        return JsonResponse({"message": "Embeddings created successfully.", "embedding_id": embedding.identificador})

    return JsonResponse({"message": "Authentication required."}, status=401)


@login_required
@require_POST
def talk_pdf(request):
    identificador = request.POST.get('identificador')
    question = request.POST.get('question')
    
    #Aqui se deberia guardar en la BD el mensaje del usuario
    save_history_user(identificador,question)

    answer = answer_question(identificador, question)
    
    #Aqui se guarda la respuesta del BOT en la BD
    save_history_bot(identificador, answer)
    

    return JsonResponse({'answer': answer}) 



