import pandas as pd
import os, tiktoken, openai, io, requests, random, string
import numpy as np
from PyPDF2 import PdfReader
from .models import Embedding, ChatHistory
from chatbot.models import Usuario
from sklearn.metrics.pairwise import cosine_similarity
from django.core.exceptions import ObjectDoesNotExist







openai.api_key = ""
tokenizer = tiktoken.get_encoding("cl100k_base")
MAX_TOKENS = 3000
MODEL = "gpt-3.5-turbo-16k"


def pdf_doc_to_text(pdf):
    reader = PdfReader(pdf)
    text = ''

    for page in reader.pages:
        text += page.extract_text()

    title = reader.metadata.get('/Title')

    return title, text




def pdf_to_text(url):
    if "drive.google.com" in url:
        file_id = url.split("/")[-2]
        response = requests.get(f"https://drive.google.com/uc?id={file_id}&export=download")
        pdf_file = io.BytesIO(response.content)
        pdf_reader = PdfReader(pdf_file)

        title = get_google_drive_file_name(url)

        text = ''
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()

        return title, text

    else:
        response = requests.get(url)
        pdf_file = io.BytesIO(response.content)
        pdf_reader = PdfReader(pdf_file)

        # Obtener el título del archivo de la URL
        title = get_file_name_from_url(url)

        text = ''
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text().encode('utf-8', 'ignore').decode('utf-8')

        return title, text

def get_google_drive_file_name(url):
    file_id = url.split("/")[-2]
    response = requests.get(f"https://drive.google.com/uc?id={file_id}&export=download")
    headers = response.headers
    content_disposition = headers.get("content-disposition")
    if content_disposition:
        filename = content_disposition.split("; filename*=UTF-8''")[-1].strip('"')
        return filename

def get_file_name_from_url(url):
    filename = url.split("/")[-1]
    return filename

def generar_caracter_aleatorio():
    caracteres = string.ascii_letters + string.digits
    caracter_aleatorio = ''.join(random.choice(caracteres) for _ in range(29))
    return caracter_aleatorio

#Funcion para limpiar lineas de texto
def remove_newlines(serie):
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie


def split_into_many(text, max_tokens=MAX_TOKENS):
    # Split the text into sentences
    sentences = text.split('. ')

    # Get the number of tokens for each sentence
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]

    chunks = []
    chunk_text = []
    tokens_so_far = 0

    # Loop through the sentences and tokens joined together in a tuple
    for sentence, token in zip(sentences, n_tokens):
        # If the number of tokens so far plus the number of tokens in the current sentence is greater
        # than the max number of tokens, then add the chunk to the list of chunks and reset
        # the chunk and tokens so far
        if tokens_so_far + token > max_tokens:
            chunks.append(chunk_text)
            chunk_text = []
            tokens_so_far = 0

        # If the number of tokens in the current sentence is greater than the max number of
        # tokens, go to the next sentence
        if token > max_tokens:
            continue

        # Otherwise, add the sentence to the chunk and add the number of tokens to the total
        chunk_text.append(sentence)
        tokens_so_far += token + 1

    # Add the last chunk to the list of chunks
    if chunk_text:
        chunks.append(chunk_text)

    return chunks


#Funcion para agregar un nuevo chunk a BD
def pdf_dfs(user_id, text, nombre_archivo, max_tokens=MAX_TOKENS):
    shortened = []

    # Tokenizar el texto y guardar el número de tokens en una nueva columna
    n_tokens = len(tokenizer.encode(text))

    # Si el número de tokens es mayor que el límite máximo, dividir el texto en chunks
    if n_tokens > max_tokens:
        chunks = split_into_many(text)
        shortened += chunks
    else:
        shortened.append(text)

    # Crear una lista de partes de texto y embeddings
    contenido_texto = []
    embeddings = []

    # Calcular los embeddings para cada chunk
    for chunk_text in shortened:
        # Calcular el embedding
        chunk_embedding = openai.Embedding.create(input=chunk_text, engine='text-embedding-ada-002')['data'][0]['embedding']
        
        # Agregar el chunk a la lista de contenido_texto
        contenido_texto.append(chunk_text)
        
        # Agregar el embedding a la lista de embeddings
        embeddings.append(chunk_embedding)

    # Crear una nueva instancia del modelo Embedding
    identificador = generar_caracter_aleatorio()
    user = Usuario.objects.get(id=user_id)
    embedding = Embedding(usuario=user, contenido_texto=contenido_texto, embeddings=embeddings, nombre_archivo=nombre_archivo, identificador=identificador)
    try:
        embedding.save()
    except ObjectDoesNotExist:
        print('Error al almacenar embeddings')
        return None
    document_get = Embedding.objects.get(identificador=identificador)
    chat_history = ChatHistory(usuario=user, document=document_get)
    chat_history.save()

def encontrar_vector_mas_similar(lista_vectores, vector_objetivo):
    lista_vectores = np.array(lista_vectores)
    vector_objetivo = np.array(vector_objetivo)

    similitudes = cosine_similarity(lista_vectores, [vector_objetivo])
    indice_mejor_similitud = np.argmax(similitudes)

    return indice_mejor_similitud

def create_context(question, identificador):
    """
    Create a context for a question by finding the most similar context from the database
    """

    # Get the embeddings for the question
    q_embedding = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']

    # Get the embeddings and chunks from the database
    embeddings_chunks = list(Embedding.objects.filter(identificador=identificador).values('embeddings', 'contenido_texto'))

    list_vectors = embeddings_chunks[0]['embeddings']

    list_text_chunks = embeddings_chunks[0]['contenido_texto']

    best_embedding_index = encontrar_vector_mas_similar(list_vectors, q_embedding)

    best_text_chunk = list_text_chunks[best_embedding_index]


    # Return the best text chunk

    return ' '.join(best_text_chunk)

def answer_question(identificador, question='', model=MODEL, debug=False):
    """
    Answer a question based on the most similar context from the database texts
    """
    context = create_context(question, identificador)

    title_pdf = Embedding.objects.get(identificador=identificador)
    
    title = title_pdf.nombre_archivo

    #Seccion para acceder al historial del chat

    document_get = Embedding.objects.get(identificador=identificador)
    chat_history = ChatHistory.objects.get(document=document_get)
    messages_hist = chat_history.historial
    messages = [{"role": "system", "content": f"Soy un chatbot amable que puede leer y responder preguntas basadas en el contexto de un PDF. Puedo complementar la respuesta con mi conocimiento pero no dar informacion diferente al PDF \n\nTitulo PDF:{title} \n\nContexto: {context}"}]
    
    for message in messages_hist:
        messages.append(message)
    #Aqui se debera consultar los datos del historial de chats para pasarlas al modelo:
    #----------------------------------------------------------------------------------

    # If debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        # Create a completions using the question and context
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return e


def save_history_user(identificador, message):
    document_get = Embedding.objects.get(identificador=identificador)
    chat_history = ChatHistory.objects.get(document=document_get)
    dict_message = {'role':'user', 'content': f'{message}'}
    historial_actual = chat_history.historial
    historial_actual.append(dict_message)
    chat_history.historial = historial_actual
    try:
        chat_history.save()
    except ObjectDoesNotExist:
        print('Error al almacenar chat')
        return None

def save_history_bot(identificador, message):
    document_get = Embedding.objects.get(identificador=identificador)
    chat_history = ChatHistory.objects.get(document=document_get)
    dict_message = {'role':'assistant', 'content': f'{message}'}
    historial_actual = chat_history.historial
    historial_actual.append(dict_message)
    chat_history.historial = historial_actual
    try:
        chat_history.save()
    except ObjectDoesNotExist:
        print('Error al almacenar chat')
        return None