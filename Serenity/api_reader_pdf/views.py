from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .utils import *

@csrf_exempt
def create_embeddings_url(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            # Usuario registrado
            pdf_text = pdf_to_text(request.POST.get('url'))

            # Crear el objeto Embedding
            embedding = Embedding(nombre_archivo=request.POST.get('nombre_archivo'),
                                  contenido_texto=pdf_text,
                                  embeddings=None,
                                  usuario=request.user)
            embedding.save()

            return JsonResponse({"message": "Embeddings creados correctamente."}, status=200)
        else:
            # Usuario no registrado
            nombre_archivo = request.POST.get('nombre_archivo')
            embeddings_count = Embedding.objects.filter(usuario__isnull=True).count()
            if embeddings_count >= 1:
                return JsonResponse({"message": "Solo se permite 1 embedding para usuarios no registrados."}, status=400)

            pdf_text = pdf_to_text(request.POST.get('url'))

            # Crear el objeto Embedding
            embedding = Embedding(nombre_archivo=nombre_archivo,
                                  contenido_texto=pdf_text,
                                  embeddings=None)
            embedding.save()

            return JsonResponse({"message": "Embeddings creados correctamente."}, status=200)

    return JsonResponse({"message": "Método no permitido."}, status=405)
