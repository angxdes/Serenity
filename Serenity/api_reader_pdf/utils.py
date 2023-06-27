import pandas as pd
import os, tiktoken, openai, io, requests, random, string
import numpy as np
from PyPDF2 import PdfReader
from .models import Embedding
from chatbot.models import Usuario
from sklearn.metrics.pairwise import cosine_similarity




openai.api_key = "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"
modelo = "text-davinci-003"
tokenizer = tiktoken.get_encoding("cl100k_base")
max_tokens = 1000


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
            text += pdf_reader.pages[page].extract_text()

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


def split_into_many(text, max_tokens=max_tokens):
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
def pdf_dfs(user_id, text, nombre_archivo):
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
    embedding.save()

def create_context(question, identificador, max_len=1000, size="ada"):
    """
    Create a context for a question by finding the most similar context from the database
    """

    # Get the embeddings for the question
    q_embedding = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']

    # Get the embeddings and chunks from the database
    embeddings_chunks = list(Embedding.objects.filter(identificador=identificador).values('embeddings', 'contenido_texto'))

    cur_len = 0
    max_similarity = float('-inf')
    best_chunk_index = -1

    # Find the most similar chunk to the question
    for index, chunk in enumerate(embeddings_chunks):
        chunk_embedding = chunk['embeddings']
        chunk_text = chunk['contenido_texto']

        # Calculate cosine similarity between chunk embedding and question embedding
        similarity = cosine_similarity(np.array(chunk_embedding), np.array(q_embedding).reshape(1, -1))[0][0]

        if similarity > max_similarity:
            max_similarity = similarity
            best_chunk_index = index

        n_tokens = sum(len(text.split()) for text in ' '.join(map(str, chunk_text)))


        # Add the length of the text to the current length
        cur_len += n_tokens + 4

        # If the context is too long, break
        if cur_len > max_len:
            break

    # Return the index of the best chunk
    return best_chunk_index

def answer_question(identificador, model="text-davinci-003", question='', max_len=1800, size="ada", debug=False, max_tokens=1000, stop_sequence=None):
    """
    Answer a question based on the most similar context from the database texts
    """
    context_index = create_context(question, identificador, max_len, size=size)

    if context_index == -1:
        return "No lo sé"

    embeddings_chunks = list(Embedding.objects.filter(identificador=identificador).values_list('contenido_texto', flat=True))
    context = "\n\n".join(embeddings_chunks[0][context_index][0])

    # If debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        # Create a completions using the question and context
        response = openai.Completion.create(
            prompt = f"Soy un chatbot que puede leer y responder preguntas basadas en el contexto de un PDF. Si no puedo responder tu pregunta, diré 'No lo sé'. Si deseas saber mi opinión, pregunta '¿Qué piensas tú?', '¿Cuál es tu punto de vista?' o algo similar. También puedes preguntarme cómo estoy o cualquier otra pregunta abierta. ¡Estoy aquí para ayudarte! \n\nContexto: {context}\n\nPregunta: {question}\n\nRespuesta: ",
            temperature=0.4,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
            model=model,
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        print(e)
        return ""
