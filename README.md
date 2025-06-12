# Chatbot de Voz para Twitch

Este proyecto implementa un asistente de voz que utiliza reconocimiento de voz, síntesis de voz y un modelo de lenguaje (Ollama) para interactuar en un chat de Twitch. El asistente puede escuchar preguntas por micrófono, transcribirlas, consultarlas a un modelo de IA y responder en voz alta.

## Requisitos

- Python 3.8 o superior
- Tener instalado y corriendo Ollama con el modelo especificado (por defecto `mistral:7b`)
- Micrófono y altavoces funcionales

## Instalación

1. Clona este repositorio.
2. Instala las dependencias ejecutando:


"pip install -r requeriments.txt"

Asegúra que Ollama esté corriendo en `http://localhost:11434` y que el modelo esté descargado.

Para utilizar la API de Ollama:

- Inicia el servidor ejecutando:  
    `ollama serve`
- Descarga el modelo necesario con:  
    `ollama pull <nombre_del_modelo>`

Asegúrate de que el servidor esté en funcionamiento antes de ejecutar el asistente.


## Uso

- Ejecuta el archivo principal:

- El asistente escuchará tu voz, transcribirá lo que digas y responderá usando el modelo de IA y síntesis de voz.

## Archivos principales

- `chat.py`: Script principal para interacción por voz.
- `botPreguntas.py`: Genera preguntas o datos aleatorios usando el modelo de IA.

## Personalización

Puedes modificar los siguientes parámetros en `chat.py`:
- `MODEL_NAME`: Nombre del modelo de Ollama.
- `API_URL`: URL de la API de Ollama.
- `INTERVALO_ESPERA`: Tiempo de espera entre interacciones.
- `DURACION_GRABACION`: Duración máxima de grabación de audio.

---