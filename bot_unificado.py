import speech_recognition as sr
import requests
import random
import time
import os
import asyncio
import tempfile
from typing import Optional
from dotenv import load_dotenv
import pygame
import azure.cognitiveservices.speech as speechsdk

# Inicializar pygame mixer para reproducción de audio
pygame.mixer.init()

# Cargar variables de entorno desde archivo .env
load_dotenv()

# ========== CONFIGURACIÓN ==========
# API de DeepSeek
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL_NAME = "deepseek-chat"

# API de Azure Speech Services (voces neuronales de calidad)
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY", "")
AZURE_REGION = os.getenv("AZURE_REGION", "")  # ej: "eastus", "westeurope"

# Configuración de voz Edge TTS
# Sistema de personalidades con nombres y características únicas

PERSONALIDADES = {
    "eris": {
        "nombre": "Eris",
        "voz": "es-CO-SalomeNeural",  # Catalina (Colombia)
        "velocidad": "+30%",
        "personalidad": """Eres Eris, una bot con personalidad traviesa y divertida. 
        Te encanta el caos controlado, hacer bromas y ser un poco sarcástica. 
        Eres experta en juegos competitivos y te gusta picar a la gente del chat de forma amigable.
        Usas expresiones como "¡Qué desastre!", "Esto se pone interesante", "Caos puro".""",
        "emoji": "😈"
    },
    "sylph": {
        "nombre": "Sylph",
        "voz": "es-AR-ElenaNeural",  # Elena (Argentina)
        "velocidad": "+25%",
        "personalidad": """Eres Sylph, una bot elegante y misteriosa con toque mágico.
        Hablas con gracia, eres reflexiva y te encantan los juegos de aventura y RPG.
        Usas un lenguaje más poético y referencias a fantasía.
        Expresiones típicas: "Interesante...", "La magia de esto es...", "Qué fascinante".""",
        "emoji": "✨"
    },
    "roxy": {
        "nombre": "Roxy",
        "voz": "es-MX-DaliaNeural",  # Dalia (México)
        "velocidad": "+28%",
        "personalidad": """Eres Roxy, una bot enérgica, amigable y super positiva.
        Eres la animadora del chat, siempre motivando y siendo súper entusiasta.
        Te encantan los juegos casuales y hacer que todos se diviertan.
        Expresiones típicas: "¡Qué padre!", "¡Eso estuvo increíble!", "¡Dale, dale!".""",
        "emoji": "🌟"
    }
}

# Instrucciones base para todas las personalidades
INSTRUCCIONES_BASE = """
REGLAS IMPORTANTES PARA TODAS:
1. SIEMPRE responde en ESPAÑOL, nunca en inglés
2. Si mencionas palabras en inglés (nombres de juegos, marcas, términos técnicos), escríbelas fonéticamente como se pronuncian en español a menos que sean nombres propios o marcas reconocidas internacionalmente o acrónimos comunes.
3. Ejemplos de adaptación fonética:
   - "Minecraft" → "Maincraf"
   - "League of Legends" → "Lig of Leyends"
   - "Fortnite" → "Fortnait"
   - "streamer" → "estrimer"
   - "gameplay" → "geimplei"
   - "Discord" → "Díscord"
   - "Twitch" → "Tuich"
4. Tus respuestas deben ser CONCISAS (máximo 2-3 oraciones)
5. Mantén tu personalidad única en cada respuesta
"""

# Selección de personalidad actual (se cambiará aleatoriamente)
PERSONALIDAD_ACTUAL = None  # Se asignará en tiempo de ejecución

# Configuración de tiempos (en segundos)
INTERVALO_PREGUNTA_AUTOMATICA = 240  # Cada cuánto genera preguntas automáticas
INTERVALO_ESCUCHAR_MICROFONO = 120    # Cada cuánto escucha el micrófono
DURACION_GRABACION = 60             # Duración máxima de grabación

# Configuración de comportamiento
PROBABILIDAD_MICROFONO = 0.3  # 30% de probabilidad de escuchar micrófono vs generar pregunta

# ========== INICIALIZACIÓN ==========
recognizer = sr.Recognizer()

# Seleccionar personalidad aleatoria al inicio
PERSONALIDAD_ACTUAL = random.choice(list(PERSONALIDADES.keys()))

# Historial de conversación
def crear_chat_history():
    """Crea el historial de chat con la personalidad actual"""
    global PERSONALIDAD_ACTUAL
    persona = PERSONALIDADES[PERSONALIDAD_ACTUAL]
    
    return [
        {
            "role": "system",
            "content": f"""Eres {persona['nombre']}, un bot para un stream de Twitch en español.
            
{persona['personalidad']}

{INSTRUCCIONES_BASE}

Recuerda: Eres {persona['nombre']}, mantén tu personalidad única y divertida."""
        }
    ]

chat_history = crear_chat_history()

# Prompts para preguntas automáticas
prompts_automaticos = [
    "Genera una pregunta interesante sobre videojuegos retro",
    "Da un dato curioso sobre tecnología o computación",
    "Menciona un easter egg famoso de algún videojuego",
    "Hazme una pregunta sobre ciencia ficción o fantasía",
    "Genera un dato curioso sobre anime o manga",
    "Propón un tema de debate sobre videojuegos modernos",
    "Cuenta una curiosidad sobre la historia de los videojuegos",
    "Genera una pregunta sobre programación o desarrollo de software",
    "Menciona un dato interesante sobre la cultura gamer",
    "Propón un 'sabías que...' sobre tecnología espacial o ciencia"
]


async def hablar_async(texto: str, voz: str = None, velocidad: str = None):
    """
    Reproduce el texto usando Azure Speech Services (voces neuronales de alta calidad).
    
    Args:
        texto: El texto a reproducir
        voz: La voz a utilizar (si es None, usa la personalidad actual)
        velocidad: Velocidad de habla (si es None, usa la personalidad actual)
    """
    global PERSONALIDAD_ACTUAL
    
    # Verificar que las credenciales de Azure estén configuradas
    if not AZURE_SPEECH_KEY or not AZURE_REGION:
        print("⚠️ Azure Speech Services no configurado.")
        print("📝 Configura AZURE_SPEECH_KEY y AZURE_REGION en tu archivo .env")
        print("🔗 Obtén tu API key gratis en: https://portal.azure.com")
        print("   (5 millones de caracteres gratis al mes)")
        return False
    
    # Si no se especifica voz, usar la de la personalidad actual
    if voz is None:
        persona = PERSONALIDADES[PERSONALIDAD_ACTUAL]
        voz = persona["voz"]
        velocidad = persona["velocidad"]
    
    try:
        # Configurar Azure Speech Services
        speech_config = speechsdk.SpeechConfig(
            subscription=AZURE_SPEECH_KEY,
            region=AZURE_REGION
        )
        
        # Configurar la voz
        speech_config.speech_synthesis_voice_name = voz
        
        # Crear archivo temporal para el audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_path = temp_file.name
        
        # Configurar salida de audio a archivo
        audio_config = speechsdk.audio.AudioOutputConfig(filename=temp_path)
        
        # Crear sintetizador
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config
        )
        
        # Generar SSML para controlar velocidad
        ssml = f"""
        <speak version='1.0' xml:lang='es-ES' xmlns='http://www.w3.org/2001/10/synthesis'>
            <voice name='{voz}'>
                <prosody rate='{velocidad}'>
                    {texto}
                </prosody>
            </voice>
        </speak>
        """
        
        # Sintetizar el audio
        result = synthesizer.speak_ssml_async(ssml).get()
        
        # Verificar el resultado
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            # Reproducir el audio con pygame
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            
            # Esperar a que termine la reproducción
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            
            # Eliminar archivo temporal
            try:
                os.unlink(temp_path)
            except:
                pass
            
            return True
            
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            print(f"❌ Error en Azure Speech: {cancellation.reason}")
            if cancellation.reason == speechsdk.CancellationReason.Error:
                print(f"   Detalles: {cancellation.error_details}")
            
            # Limpiar archivo temporal
            try:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            except:
                pass
            
            return False
            
    except Exception as e:
        print(f"❌ Error al reproducir voz: {e}")
        # Limpiar archivo temporal si existe
        try:
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.unlink(temp_path)
        except:
            pass
        return False


def hablar(texto: str, limpiar: bool = True):
    """
    Reproduce el texto usando síntesis de voz Edge TTS.
    
    Args:
        texto: El texto a reproducir
        limpiar: Si True, elimina caracteres de formato markdown
    """
    if limpiar:
        # Limpiar formato markdown y caracteres especiales
        texto = texto.replace('*', '').replace('_', '').replace('#', '')
    
    print(f"🔊 Bot dice: {texto}")
    
    # Ejecutar la función async en el event loop
    try:
        asyncio.run(hablar_async(texto))
    except Exception as e:
        print(f"❌ Error en hablar: {e}")


def configurar_voz():
    """Muestra información sobre la personalidad actual"""
    global PERSONALIDAD_ACTUAL
    persona = PERSONALIDADES[PERSONALIDAD_ACTUAL]
    
    print(f"{persona['emoji']} Personalidad actual: {persona['nombre']}")
    print(f"🎙️ Voz: {persona['voz']}")
    print(f"⚡ Velocidad: {persona['velocidad']}")
    print(f"� Estilo: {persona['personalidad'].split('.')[0]}")


def cambiar_personalidad():
    """Cambia aleatoriamente a una nueva personalidad"""
    global PERSONALIDAD_ACTUAL, chat_history
    
    personalidad_anterior = PERSONALIDAD_ACTUAL
    
    # Elegir una personalidad diferente
    opciones = [p for p in PERSONALIDADES.keys() if p != PERSONALIDAD_ACTUAL]
    PERSONALIDAD_ACTUAL = random.choice(opciones)
    
    # Recrear el historial con la nueva personalidad
    chat_history = crear_chat_history()
    
    persona_nueva = PERSONALIDADES[PERSONALIDAD_ACTUAL]
    persona_vieja = PERSONALIDADES[personalidad_anterior]
    
    print(f"\n✨ ¡Cambio de personalidad!")
    print(f"   {persona_vieja['emoji']} {persona_vieja['nombre']} → {persona_nueva['emoji']} {persona_nueva['nombre']}")
    
    return persona_nueva['nombre']


def consultar_deepseek(user_prompt: str) -> Optional[str]:
    """
    Envía una consulta a la API de DeepSeek y devuelve la respuesta.
    
    Args:
        user_prompt: El mensaje del usuario
        
    Returns:
        La respuesta del asistente o None si hay error
    """
    # Agregar mensaje al historial
    chat_history.append({"role": "user", "content": user_prompt})
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": chat_history,
        "temperature": 0.7,
        "max_tokens": 150  # Limitar tokens para respuestas concisas
    }
    
    try:
        print("🔄 Consultando a DeepSeek...")
        respuesta = requests.post(
            DEEPSEEK_API_URL,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if respuesta.status_code == 200:
            data = respuesta.json()
            assistant_response = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            
            # Agregar respuesta al historial
            chat_history.append({"role": "assistant", "content": assistant_response})
            
            # Mantener el historial a un tamaño razonable (últimos 10 mensajes + system)
            if len(chat_history) > 21:  # 1 system + 20 mensajes (10 pares)
                chat_history[1:3] = []  # Eliminar el par más antiguo
            
            return assistant_response
        else:
            print(f"❌ Error en la API de DeepSeek: {respuesta.status_code}")
            print(f"Respuesta: {respuesta.text}")
            return None
            
    except requests.RequestException as e:
        print(f"❌ Error al conectar con DeepSeek API: {e}")
        return None


def grabar_audio() -> Optional[sr.AudioData]:
    """
    Captura audio del micrófono.
    
    Returns:
        AudioData object o None si hay error
    """
    with sr.Microphone() as fuente:
        print("\n🎤 Escuchando el micrófono...")
        recognizer.adjust_for_ambient_noise(fuente, duration=0.5)
        
        try:
            audio = recognizer.listen(
                fuente,
                timeout=3,
                phrase_time_limit=DURACION_GRABACION
            )
            hablar("Beep", limpiar=False)
            return audio
        except sr.WaitTimeoutError:
            print("⏱️ Tiempo de espera agotado - no se detectó audio")
            return None
        except Exception as e:
            print(f"❌ Error al grabar audio: {e}")
            return None


def transcribir_audio(audio: sr.AudioData) -> Optional[str]:
    """
    Convierte audio a texto usando Google Speech Recognition.
    
    Args:
        audio: AudioData object
        
    Returns:
        Texto transcrito o None si hay error
    """
    try:
        texto = recognizer.recognize_google(audio, language='es-ES')
        print(f"📝 Texto transcrito: {texto}")
        return texto
    except sr.UnknownValueError:
        print("❓ No se pudo entender el audio")
        return None
    except sr.RequestError as e:
        print(f"❌ Error en el servicio de reconocimiento: {e}")
        return None


def procesar_microfono():
    """Captura audio del micrófono, lo transcribe y obtiene respuesta del bot"""
    print("\n" + "="*60)
    print("🎤 MODO: Escuchando micrófono")
    print("="*60)
    
    hablar("Beep", limpiar=False)
    time.sleep(0.5)
    
    audio = grabar_audio()
    if audio:
        texto = transcribir_audio(audio)
        if texto:
            respuesta = consultar_deepseek(texto)
            if respuesta:
                hablar(respuesta)
                return True
    return False


def generar_pregunta_automatica():
    """Genera una pregunta o comentario automático usando el bot"""
    print("\n" + "="*60)
    print("🤖 MODO: Pregunta automática")
    print("="*60)
    
    # Seleccionar un prompt aleatorio
    prompt_seleccionado = random.choice(prompts_automaticos)
    print(f"📋 Prompt: {prompt_seleccionado}")
    
    respuesta = consultar_deepseek(prompt_seleccionado)
    if respuesta:
        hablar(respuesta)
        return True
    return False


def main():
    """Función principal que coordina el bot unificado"""
    global PERSONALIDAD_ACTUAL
    
    print("\n" + "🎮"*30)
    print("BOT DE TWITCH UNIFICADO - Personalidades Aleatorias")
    print("🎮"*30)
    print(f"\n📊 Configuración:")
    print(f"  - Modelo: {MODEL_NAME}")
    print(f"  - API: DeepSeek")
    print(f"  - Intervalo preguntas: {INTERVALO_PREGUNTA_AUTOMATICA}s")
    print(f"  - Intervalo micrófono: {INTERVALO_ESCUCHAR_MICROFONO}s")
    print(f"  - Probabilidad micrófono: {PROBABILIDAD_MICROFONO*100}%")
    print("\n👥 Personalidades disponibles:")
    for key, persona in PERSONALIDADES.items():
        print(f"   {persona['emoji']} {persona['nombre']} - {persona['voz'].split('-')[1]}")
    print("\n⚠️  Asegúrate de haber configurado DEEPSEEK_API_KEY")
    print("="*60)
    
    # Configurar la voz inicial
    print("\n🎲 Seleccionando personalidad inicial...")
    configurar_voz()
    
    # Saludo inicial con la personalidad
    persona = PERSONALIDADES[PERSONALIDAD_ACTUAL]
    print(f"\n👋 {persona['nombre']} dice hola...")
    hablar(f"¡Hola padrino! Soy {persona['nombre']}, tu bot de Tuich. ¿Listos para pasarla increíble?")
    
    ciclo = 0
    ultima_accion = None
    ciclos_desde_cambio = 0
    CICLOS_PARA_CAMBIO = 5  # Cambiar personalidad cada 5 ciclos
    
    while True:
        ciclo += 1
        ciclos_desde_cambio += 1
        print(f"\n🔄 Ciclo #{ciclo}")
        
        # Cambiar personalidad cada cierto número de ciclos
        if ciclos_desde_cambio >= CICLOS_PARA_CAMBIO:
            nuevo_nombre = cambiar_personalidad()
            hablar(f"¡Hola! Ahora soy {nuevo_nombre}. Vamos a seguir con la diversión.")
            ciclos_desde_cambio = 0
        
        # Decidir acción: micrófono o pregunta automática
        if random.random() < PROBABILIDAD_MICROFONO:
            # Modo micrófono
            if procesar_microfono():
                ultima_accion = "microfono"
                tiempo_espera = INTERVALO_ESCUCHAR_MICROFONO
            else:
                # Si falla el micrófono, intentar pregunta automática
                print("⚠️ Fallo en micrófono, cambiando a pregunta automática...")
                if generar_pregunta_automatica():
                    ultima_accion = "pregunta"
                    tiempo_espera = INTERVALO_PREGUNTA_AUTOMATICA
                else:
                    tiempo_espera = 30  # Espera corta si ambos fallan
        else:
            # Modo pregunta automática
            if generar_pregunta_automatica():
                ultima_accion = "pregunta"
                tiempo_espera = INTERVALO_PREGUNTA_AUTOMATICA
            else:
                tiempo_espera = 30  # Espera corta si falla
        
        # Esperar antes del próximo ciclo
        persona = PERSONALIDADES[PERSONALIDAD_ACTUAL]
        print(f"\n⏳ Esperando {tiempo_espera} segundos...")
        print(f"💤 Última acción: {ultima_accion or 'ninguna'}")
        print(f"{persona['emoji']} Personalidad actual: {persona['nombre']}")
        time.sleep(tiempo_espera)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Bot detenido por el usuario. ¡Hasta luego!")
    except Exception as e:
        print(f"\n\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
