<h1 align="center">Serenity</h1>

## Índice

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Características Principales](#características-principales)
- [Instalación](#instalación)
- [Contribución](#contribución)

## Descripción del Proyecto

<p>
  El proyecto es una implementación de inteligencia artificial que busca crear expertos virtuales en diversos temas con el objetivo de ayudar a las empresas a optimizar su trabajo. Esta solución permite interactuar con estos expertos a través de chat, admitiendo el envío y análisis de diferentes tipos de archivos, como PDF, imágenes y videos.
</p>

## Características Principales

<ul>
  <li><strong>Interacción en tiempo real:</strong> Los usuarios pueden chatear directamente con los expertos virtuales, realizando consultas, obteniendo recomendaciones y recibiendo respuestas de manera instantánea.</li>
  <li><strong>Soporte para múltiples formatos:</strong> El sistema es capaz de procesar y analizar archivos en diferentes formatos, como PDF, imágenes y videos, para extraer información relevante y brindar respuestas precisas y contextualizadas.</li>
  <li><strong>Embeddings de contenido:</strong> Mediante técnicas de procesamiento de lenguaje natural y aprendizaje automático, el proyecto realiza embeddings de los archivos y mensajes enviados, lo que permite una mejor comprensión y análisis del contenido.</li>
  <li><strong>Optimización del trabajo:</strong> Al contar con expertos virtuales especializados, las empresas pueden mejorar la eficiencia y calidad de su trabajo al tener acceso a conocimientos y recomendaciones específicas en tiempo real.</li>
</ul>

<p>
  El proyecto combina las tecnologías de inteligencia artificial, procesamiento de lenguaje natural y análisis de datos para crear una solución completa y versátil que brinda asistencia experta a las empresas en diversas áreas.
</p>


## Instalación

<p>Sigue los siguientes pasos para instalar y configurar el proyecto en tu entorno local:</p>


<ol>
  <li>Clona el repositorio en tu máquina local utilizando el siguiente comando:</li>
  <pre><code>git clone https://github.com/angxdes/Serenity2.0</code></pre>
  
  <li>Accede al directorio del proyecto:</li>
  <pre><code>cd Serenity</code></pre>
  
  <li> Crea una carpeta llamada venv </li>
   <pre><code>mkdir venv</code></pre>
  
  <li>Accede al directorio del proyecto:</li>
  <pre><code>cd venv</code></pre>
  
  <li>Crea un entorno virtual utilizando <code>venv</code> (asegúrate de tener Python 3 instalado):</li>
  <pre><code>python3 -m venv venv</code> o <code>python -m venv venv</code></pre>
  
  <li>En el archivo .gitignore introduce la carpeta venv, tu archivo debera tener una linea asi: </li>
  <pre><code>
  venv/
*.pyc
__pycache__/
  </code></pre>
  
  <li>Activa el entorno virtual:</li>
  <ul>
    <li>En macOS y Linux:</li>
    <pre><code>source venv/bin/activate</code></pre>
    <li>En Windows:</li>
    <pre><code>venv\Scripts\activate</code></pre>
  </ul>
  
  <li>Instala las dependencias necesarias:</li>
  <pre><code>pip install -r requirements.txt</code></pre>
  
  <li>Entra a la carpeta del proyecto en Django:</li>
  <pre><code>cd Serenity</code></pre>
  
  <li>¡Listo! Ahora puedes ejecutar el proyecto utilizando el siguiente comando:</li>
  <pre><code>python3 manage.py runserver</code></pre>
  <p>O</p>
  <pre><code>python manage.py runserver</code></pre>
</ol>

## Contribución

<p>¡Gracias por tu interés en contribuir a este proyecto! A continuación, se presentan algunas pautas para ayudarte a empezar:</p>

<ul>
  <li>Si encuentras un error o tienes una idea para una mejora, por favor, abre un issue en el repositorio. Asegúrate de proporcionar detalles claros y concisos sobre el problema o la sugerencia.</li>
  <li>Si deseas trabajar en una tarea existente, comenta en el issue correspondiente para informar a los demás de tu intención y evitar duplicados de esfuerzo.</li>
  <li>Si deseas contribuir con código, sigue estos pasos:
    <ol>
      <li>Haz un fork de este repositorio y clónalo en tu máquina local.</li>
      <li>Crea una nueva rama para tu contribución: <code>git checkout -b mi-contribucion</code>.</li>
      <li>Realiza tus cambios y asegúrate de que el código sigue las convenciones de estilo existentes.</li>
      <li>Realiza commits descriptivos y claros.</li>
      <li>Envía un pull request a la rama <code>main</code> de este repositorio, describiendo los cambios realizados y cualquier información relevante.</li>
    </ol>
  </li>
  <li>Se valoran y aprecian todas las contribuciones, ya sea en forma de código, documentación, corrección de errores, pruebas, sugerencias o comentarios.</li>
</ul>

<p>Agradecemos mucho todas las contribuciones, grandes o pequeñas. Juntos podemos hacer crecer este proyecto y mejorar su funcionalidad para beneficiar a la comunidad.</p>



<p align="center">
<em>¡Disfruta del proyecto!</em>
</p>
