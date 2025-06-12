import speech_recognition as sr
import requests
import pyttsx3
import random
import time


# Configuración
MODEL_NAME = "mistral:7b"  # Cambia por el modelo que uses
API_URL = "http://localhost:11434/api/chat"  # URL de la API de Ollama
INTERVALO_ESPERA = 120  # Segundos entre capturas de audio

# Historial de conversación para mantener el contexto
chat_history = [
    {"role": "system", "content": "Eres un asistente amigable y serio para un chat de Twitch. Saluda diciendo: 'Hola padrino, ¿en qué puedo ayudarte hoy?'"}
]



motor_voz = pyttsx3.init()

promts = ["Genera una pregunta aleatoria","Da un dato importante geek","Menciona datos de un videojuego famoso", "Hazme una pregunta sobre un tema de ciencia o computacion", "Genera un haiku de caballos"]

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
    """Reproduce el texto usando síntesis de voz"""
    motor_voz.setProperty('rate', 250)
    motor_voz.setProperty('volume', 1.0)
    
    # Configuración adicional para salida directa
    motor_voz.setProperty('voice', 'Microsoft Said Desktop')  # Ejemplo para Windows
    
    motor_voz.say(texto)
    motor_voz.runAndWait()

def main():
    print("Sistema de asistencia por voz activado")
    print(f"Configuración actual:\n- Modelo: {MODEL_NAME}\n- Intervalo: {INTERVALO_ESPERA}s\n")
    
    while True:
        random.seed()  # Inicializar generador de números aleatorios
        texto = "Eres un chatbot de convivencia para twich, esta es tu instruccion solo genera lo que se te pide: " + promts[random.randint(0, len(promts)-1)]

        print(f"Pregunta generada: {texto}")

        print("Consultando a Ollama...")
        respuesta = consultar_ollama(texto)
                
        if respuesta:
            #  Reproducir respuesta
            print(f"Respuesta: {respuesta}")
            hablar(respuesta)
        
        # Esperar antes de la próxima captura
        time.sleep(INTERVALO_ESPERA)

if __name__ == "__main__":
    main()