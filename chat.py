import speech_recognition as sr
import requests
import pyttsx3
import time

# Configuración de parámetros principales
#Se pueden modificar los siguientes parámetros según sea necesario
MODEL_NAME = "mistral:7b"  # Nombre del modelo a utilizar
API_URL = "http://localhost:11434/api/chat"  # URL de la API de Ollama
INTERVALO_ESPERA = 60  # Segundos entre capturas de audio
DURACION_GRABACION = 580  # Segundos para grabar audio

# Inicialización de componentes de reconocimiento y síntesis de voz
recognizer = sr.Recognizer()
motor_voz = pyttsx3.init()

# Historial de conversación para mantener el contexto
chat_history = [
    {"role": "system", "content": "Eres un asistente amigable y serio para un chat de Twitch. Saluda diciendo: 'Hola padrino, ¿en qué puedo ayudarte hoy?'"}
]

def grabar_audio():
    """
    Captura audio del micrófono y lo devuelve como objeto AudioData.
    """
    with sr.Microphone() as fuente:
        print("\nEscuchando...")
        try:
            audio = recognizer.listen(
                fuente,
                timeout=3,
                phrase_time_limit=DURACION_GRABACION + 5  # Añadir un margen de 5 segundos
            )

            hablar("Piip")
            return audio
        except sr.WaitTimeoutError:
            print("Tiempo de espera agotado")
            return None

def transcribir_audio(audio):
    """
    Convierte el audio capturado a texto usando Google Speech Recognition.
    """
    try:
        texto = recognizer.recognize_google(audio, language='es-ES')
        print(f"Texto detectado: {texto}")
        return texto
    except sr.UnknownValueError:
        print("No se pudo entender el audio")
        return None
    except sr.RequestError as e:
        print(f"Error en el servicio de reconocimiento: {e}")
        return None

def consultar_ollama(user_prompt):
    """
    Envía la consulta de usuario a la API de Ollama y devuelve la respuesta del asistente.
    """
    chat_history.append({"role": "user", "content": user_prompt})

    try:
        respuesta = requests.post(
            API_URL,
            json={
                "model": MODEL_NAME,
                "messages": chat_history,
                "stream": False
            },
            timeout=150,
            headers={"Content-Type": "application/json"}
        )
        if respuesta.status_code == 200:
            assistant_response = respuesta.json().get("message", {}).get("content", "").strip()
            chat_history.append({"role": "assistant", "content": assistant_response})
            return assistant_response
        else:
            print(f"Error en la API: {respuesta.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None

def hablar(texto):
    """
    Reproduce el texto recibido usando síntesis de voz.
    """
    texto = texto.replace('*', '').replace('_', '')
    motor_voz.setProperty('rate', 275)  # Velocidad de habla
    motor_voz.say(texto)
    motor_voz.runAndWait()

def main():
    """
    Función principal que coordina la captura de audio, transcripción, consulta a la API y síntesis de voz.
    """
    print("Sistema de asistencia por voz activado")
    print(f"Configuración actual:\n- Modelo: {MODEL_NAME}\n- Intervalo: {INTERVALO_ESPERA}s\n")
    while True:
        print("\nIniciando grabación de audio...")
        hablar("piip")
        time.sleep(1)
        audio = grabar_audio()
        if audio:
            texto = transcribir_audio(audio)
            if texto:
                print("Consultando a Ollama...")
                respuesta = consultar_ollama(texto)
                if respuesta:
                    print(f"Respuesta: {respuesta}")
                    hablar(respuesta)
        time.sleep(INTERVALO_ESPERA)

if __name__ == "__main__":
    main()
