#!/usr/bin/env python3
"""
Demo de voces Edge TTS - Prueba diferentes voces en español
Ejecuta este script para escuchar las diferentes voces disponibles
"""

import asyncio
import edge_tts
import tempfile
import os
import pygame

# Inicializar pygame mixer
pygame.mixer.init()

# Voces en español disponibles (las mejores y más naturales)
VOCES_ESPAÑOL = {
    "Jorge (México - Masculina, Amigable)": "es-MX-JorgeNeural",
    "Dalia (México - Femenina, Cálida)": "es-MX-DaliaNeural",
    "Álvaro (España - Masculina, Seria)": "es-ES-AlvaroNeural",
    "Elvira (España - Femenina, Clara)": "es-ES-ElviraNeural",
    "Tomás (Argentina - Masculina)": "es-AR-TomasNeural",
    "Elena (Argentina - Femenina)": "es-AR-ElenaNeural",
    "Catalina (Colombia - Femenina)": "es-CO-SalomeNeural",
    "Gonzalo (Colombia - Masculina)": "es-CO-GonzaloNeural",
}

TEXTO_PRUEBA = "¡Hola padrino! Soy un bot de Twitch. ¿Sabías que Edge TTS tiene voces muy naturales?"


async def probar_voz(nombre: str, voz_id: str):
    """Prueba una voz específica"""
    print(f"\n🎙️ Probando: {nombre}")
    print(f"   ID: {voz_id}")
    print(f"   Texto: {TEXTO_PRUEBA}")
    print("   ▶️ Reproduciendo...")
    
    try:
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_path = temp_file.name
        
        # Generar audio
        communicate = edge_tts.Communicate(TEXTO_PRUEBA, voz_id)
        await communicate.save(temp_path)
        
        # Reproducir con pygame
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        
        # Esperar a que termine
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
        
        # Limpiar
        os.unlink(temp_path)
        
        print("   ✅ Completado")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")


async def main():
    """Función principal"""
    print("\n" + "="*70)
    print("🎤 DEMO DE VOCES EDGE TTS - Voces en Español")
    print("="*70)
    print(f"\nSe probarán {len(VOCES_ESPAÑOL)} voces diferentes.")
    print("Escucha cada una y decide cuál te gusta más.\n")
    
    input("Presiona Enter para comenzar...")
    
    for nombre, voz_id in VOCES_ESPAÑOL.items():
        await probar_voz(nombre, voz_id)
        
        # Pausa entre voces
        if nombre != list(VOCES_ESPAÑOL.keys())[-1]:  # Si no es la última
            print("\n⏳ Pausa de 2 segundos...")
            await asyncio.sleep(2)
    
    print("\n" + "="*70)
    print("✅ Demo completada!")
    print("\n💡 Para usar una voz específica en el bot:")
    print("   Edita 'bot_unificado.py' y cambia la variable VOZ_EDGE_TTS")
    print("   Ejemplo: VOZ_EDGE_TTS = 'es-MX-JorgeNeural'")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
