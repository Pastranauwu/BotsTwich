#!/usr/bin/env python3
"""
Script de prueba del bot principal
Ejecuta 3 ciclos rápidos para probar funcionamiento
"""

import speech_recognition as sr
import requests
import random
import time
import os
import asyncio
import edge_tts
import tempfile
from typing import Optional
from dotenv import load_dotenv
import pygame

# Cargar variables de entorno
load_dotenv()

# Inicializar pygame
pygame.mixer.init()

# Configuración
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL_NAME = "deepseek-chat"

# Configuración de voz
VOZ_EDGE_TTS = "es-CO-SalomeNeural"  # Catalina
VOZ_VELOCIDAD = "+30%"  # Velocidad óptima

# Para prueba: tiempos más cortos
INTERVALO_ENTRE_CICLOS = 5  # Solo 5 segundos entre ciclos
NUMERO_CICLOS = 3  # Solo 3 ciclos de prueba

# Historial de conversación
chat_history = [
    {
        "role": "system", 
        "content": """Eres un bot interactivo y divertido para un stream de Twitch en español. 
        
        REGLAS IMPORTANTES:
        1. SIEMPRE responde en ESPAÑOL, nunca en inglés
        2. Si mencionas palabras en inglés (nombres de juegos, marcas, términos técnicos), escríbelas fonéticamente como se pronuncian en español
        3. Ejemplos de adaptación fonética:
           - "Minecraft" → "Maincraf"
           - "League of Legends" → "Lig of Leyends"
           - "Fortnite" → "Fortnait"
           - "streamer" → "estrimer"
           - "gameplay" → "geimplei"
           - "bug" → "bag"
           - "GTA" → "yi ti ei"
           - "Discord" → "Díscord"
        4. Mantén un tono amigable, geek y casual
        5. Tus respuestas deben ser CONCISAS (máximo 2-3 oraciones)
        6. Usa lenguaje cercano, como si hablaras con amigos del chat
        
        Recuerda: El objetivo es que la voz en español suene natural al leer TODO en español."""
    }
]

# Prompts de prueba
prompts_prueba = [
    "Di un saludo divertido mencionando Twitch y streamers",
    "Menciona un dato curioso sobre Minecraft o Fortnite",
    "Habla sobre algún videojuego popular como League of Legends o GTA"
]


async def hablar_async(texto: str):
    """Reproduce texto con Edge TTS"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_path = temp_file.name
        
        communicate = edge_tts.Communicate(texto, VOZ_EDGE_TTS, rate=VOZ_VELOCIDAD)
        await communicate.save(temp_path)
        
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
        
        os.unlink(temp_path)
        
    except Exception as e:
        print(f"❌ Error al reproducir voz: {e}")


def hablar(texto: str, limpiar: bool = True):
    """Wrapper para función async"""
    if limpiar:
        texto = texto.replace('*', '').replace('_', '').replace('#', '')
    
    print(f"🔊 Bot dice: {texto}")
    
    try:
        asyncio.run(hablar_async(texto))
    except Exception as e:
        print(f"❌ Error en hablar: {e}")


def consultar_deepseek(user_prompt: str) -> Optional[str]:
    """Consulta a DeepSeek"""
    chat_history.append({"role": "user", "content": user_prompt})
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": chat_history,
        "temperature": 0.7,
        "max_tokens": 150
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
            chat_history.append({"role": "assistant", "content": assistant_response})
            
            if len(chat_history) > 21:
                chat_history[1:3] = []
            
            return assistant_response
        else:
            print(f"❌ Error en la API: {respuesta.status_code}")
            return None
            
    except requests.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return None


def main():
    """Función de prueba"""
    print("\n" + "🎮"*30)
    print("PRUEBA DEL BOT DE TWITCH")
    print("🎮"*30)
    print(f"\n📊 Configuración de Prueba:")
    print(f"  - Voz: {VOZ_EDGE_TTS} (Catalina)")
    print(f"  - Velocidad: {VOZ_VELOCIDAD}")
    print(f"  - Ciclos: {NUMERO_CICLOS}")
    print(f"  - Intervalo: {INTERVALO_ENTRE_CICLOS}s")
    print("="*60)
    
    # Saludo inicial
    print("\n👋 Iniciando bot...")
    hablar("Hola padrino, este es un test del bot de Twitch. Vamos a hacer algunas preguntas de prueba.")
    
    for ciclo in range(1, NUMERO_CICLOS + 1):
        print(f"\n🔄 Ciclo #{ciclo} de {NUMERO_CICLOS}")
        print("="*60)
        
        # Seleccionar prompt
        prompt = prompts_prueba[(ciclo - 1) % len(prompts_prueba)]
        print(f"📋 Prompt: {prompt}")
        
        # Obtener respuesta
        respuesta = consultar_deepseek(prompt)
        
        if respuesta:
            print(f"✅ Respuesta obtenida")
            hablar(respuesta)
        else:
            print("❌ No se obtuvo respuesta")
        
        # Esperar antes del siguiente ciclo
        if ciclo < NUMERO_CICLOS:
            print(f"\n⏳ Esperando {INTERVALO_ENTRE_CICLOS} segundos...\n")
            time.sleep(INTERVALO_ENTRE_CICLOS)
    
    print("\n" + "="*60)
    print("✅ Prueba completada!")
    print("\n💡 Si todo funcionó bien:")
    print("   - Ejecuta: python3 bot_unificado.py")
    print("   - Para usar en tu stream")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Prueba detenida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
