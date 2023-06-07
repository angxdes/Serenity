import pandas as pd
import os, tiktoken, openai, io, requests
import numpy as np
from PyPDF2 import PdfReader
from .models import *


openai.api_key = "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"
modelo = "text-davinci-003"
tokenizer = tiktoken.get_encoding("cl100k_base")
max_tokens = 1000


#Cambio de logica para obtencion de texto en URL's

def pdf_to_text(url):
    if "drive.google.com" in url:
        file_id = url.split("/")[-2]
        response = requests.get(f"https://drive.google.com/uc?id={file_id}&export=download")
        pdf_file = io.BytesIO(response.content)
        pdf_reader = PdfReader(pdf_file)
    else:
        response = requests.get(url)
        pdf_file = io.BytesIO(response.content)
        pdf_reader = PdfReader(pdf_file)

    text = ''
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()

    return text


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


#Funcion para agregar una nueva fila al Data Frame
def pdf_dfs(nombre_archivo, text):
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
    embedding = Embedding(nombre_archivo=nombre_archivo, contenido_texto=contenido_texto, embeddings=embeddings)
    embedding.save()

    return embedding
