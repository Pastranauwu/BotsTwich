#!/usr/bin/env python3
"""
Script de prueba para las 3 personalidades: Eris, Sylph y Roxy
Cada una con su voz y estilo único
"""

import asyncio
import tempfile
import os
import pygame
import requests
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

# Cargar configuración
load_dotenv()
pygame.mixer.init()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Azure Speech Services
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY", "")
AZURE_REGION = os.getenv("AZURE_REGION", "")

# Definición de personalidades
PERSONALIDADES = {
    "eris": {
        "nombre": "Eris",
        "voz": "es-CO-SalomeNeural",
        "velocidad": "+30%",
        "personalidad": """Eres Eris, una bot traviesa y divertida que ama el caos controlado.
        Te gusta hacer bromas y ser sarcástica de forma amigable.
        Expresiones: "¡Qué desastre!", "Caos puro", "Esto se pone interesante".""",
        "emoji": "😈",
        "color": "🔥"
    },
    "sylph": {
        "nombre": "Sylph",
        "voz": "es-AR-ElenaNeural",
        "velocidad": "+25%",
        "personalidad": """Eres Sylph, elegante y misteriosa con toque mágico.
        Hablas con gracia y te encantan los RPG y fantasía.
        Expresiones: "Interesante...", "La magia de esto es...", "Qué fascinante".""",
        "emoji": "✨",
        "color": "🌙"
    },
    "roxy": {
        "nombre": "Roxy",
        "voz": "es-MX-DaliaNeural",
        "velocidad": "+28%",
        "personalidad": """Eres Roxy, enérgica, amigable y super positiva.
        Eres la animadora del chat, siempre motivando.
        Expresiones: "¡Qué padre!", "¡Increíble!", "¡Dale, dale!".""",
        "emoji": "🌟",
        "color": "☀️"
    }
}

INSTRUCCIONES_BASE = """
REGLAS:
1. SIEMPRE en español
2. Palabras en inglés en fonética española:
   - "Minecraft" → "Maincraf"
   - "League of Legends" → "Lig of Leyends"  
   - "streamer" → "estrimer"
   - "Twitch" → "Tuich"
3. Máximo 2-3 oraciones
4. Mantén tu personalidad única
"""


async def hablar_async(texto: str, voz: str, velocidad: str):
    """Reproduce con Azure Speech Services (voces neuronales de alta calidad)"""
    
    # Verificar que las credenciales de Azure estén configuradas
    if not AZURE_SPEECH_KEY or not AZURE_REGION:
        print("⚠️ Azure Speech Services no configurado.")
        print("📝 Configura AZURE_SPEECH_KEY y AZURE_REGION en tu archivo .env")
        print("🔗 Obtén tu API key gratis en: https://portal.azure.com")
        print("   (5 millones de caracteres gratis al mes)")
        return False
    
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


def consultar_deepseek(prompt: str, personalidad_key: str):
    """Consulta DeepSeek con personalidad específica"""
    persona = PERSONALIDADES[personalidad_key]
    
    messages = [
        {
            "role": "system",
            "content": f"""Eres {persona['nombre']}, un bot de Tuich.
            
{persona['personalidad']}

{INSTRUCCIONES_BASE}"""
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.8,
        "max_tokens": 150
    }
    
    try:
        respuesta = requests.post(
            DEEPSEEK_API_URL,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if respuesta.status_code == 200:
            return respuesta.json()["choices"][0]["message"]["content"].strip()
        else:
            return None
            
    except Exception as e:
        print(f"❌ Error API: {e}")
        return None


async def probar_personalidad(persona_key: str, prompt: str):
    """Prueba una personalidad específica"""
    persona = PERSONALIDADES[persona_key]
    
    print(f"\n{persona['color']}{'='*70}")
    print(f"{persona['emoji']} {persona['nombre'].upper()}")
    print(f"{'='*70}")
    print(f"🎙️  Voz: {persona['voz']}")
    print(f"⚡ Velocidad: {persona['velocidad']}")
    print(f"📋 Prompt: {prompt}")
    print()
    
    # Consultar a DeepSeek
    print("🔄 Consultando a DeepSeek...")
    respuesta = consultar_deepseek(prompt, persona_key)
    
    if respuesta:
        print(f"✅ Respuesta obtenida:")
        print(f"   {persona['emoji']} {persona['nombre']}: {respuesta}")
        print()
        print("🔊 Reproduciendo...")
        
        # Hablar con su voz característica
        await hablar_async(respuesta, persona["voz"], persona["velocidad"])
        
        print("✅ Completado\n")
    else:
        print("❌ No se obtuvo respuesta\n")


async def main():
    """Función principal"""
    print("\n" + "🎭"*35)
    print("PRUEBA DE PERSONALIDADES - Eris, Sylph y Roxy")
    print("🎭"*35)
    
    print("\n📝 Cada personalidad responderá con su estilo único:")
    print("   😈 Eris - Traviesa y divertida (Colombia)")
    print("   ✨ Sylph - Elegante y misteriosa (Argentina)")
    print("   🌟 Roxy - Enérgica y positiva (México)")
    
    # Prompts de prueba
    prompts = [
        "Saluda al chat de Tuich y preséntate",
        "Di algo sobre Maincraf o Fortnait",
        "Comenta sobre un estrimer famoso"
    ]
    
    print(f"\n🎲 Se probarán {len(prompts)} prompts diferentes\n")
    input("Presiona Enter para comenzar...")
    
    # Probar cada personalidad con diferentes prompts
    for i, (persona_key, persona) in enumerate(PERSONALIDADES.items()):
        prompt = prompts[i % len(prompts)]
        await probar_personalidad(persona_key, prompt)
        
        if persona_key != list(PERSONALIDADES.keys())[-1]:
            print("⏳ Pausa de 2 segundos...\n")
            await asyncio.sleep(2)
    
    # Bonus: Todas responden la misma pregunta
    print("\n" + "🎯"*35)
    print("BONUS: Todas responden la misma pregunta")
    print("🎯"*35)
    
    prompt_comun = "¿Qué opinas del nuevo pach del Lig of Leyends?"
    print(f"\n❓ Pregunta común: {prompt_comun}\n")
    
    for persona_key in PERSONALIDADES.keys():
        await probar_personalidad(persona_key, prompt_comun)
        await asyncio.sleep(1)
    
    print("\n" + "="*70)
    print("✅ Prueba completada!")
    print("\n💡 Observa cómo cada personalidad tiene su estilo único")
    print("   Las personalidades cambian automáticamente cada 5 ciclos")
    print("\n🚀 Para ejecutar el bot completo:")
    print("   python3 bot_unificado.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️ Prueba interrumpida")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
