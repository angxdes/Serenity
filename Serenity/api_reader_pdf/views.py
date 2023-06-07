from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .utils import *

@csrf_exempt
def create_embeddings_url(request):
    if request.method == "POST":
        url = request.POST.get("url")
        nombre_archivo = request.POST.get("nombre_archivo")
        
        if Embedding.objects.filter(nombre_archivo=nombre_archivo).exists():
            return JsonResponse({"message": "Un archivo con ese nombre ya existe"})
  
        pdf_text = pdf_to_text(url)

        # Obtener las partes de texto y embeddings y guardar en BD
        pdf_dfs(nombre_archivo, pdf_text)

        return JsonResponse({"message": "Embeddings created successfully."})
