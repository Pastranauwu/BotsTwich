#!/usr/bin/env python3
"""
Script de prueba rápida para las voces Catalina y Elena
"""

import asyncio
import edge_tts
import tempfile
import os
import pygame

# Inicializar pygame para audio
pygame.mixer.init()

async def probar_voz(nombre, voz_id, velocidad, texto):
    """Prueba una voz con velocidad específica"""
    print(f"\n🎙️ Probando: {nombre}")
    print(f"   Velocidad: {velocidad}")
    print(f"   Texto: {texto}")
    print("   ▶️ Reproduciendo...")
    
    try:
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_path = temp_file.name
        
        # Generar audio con velocidad
        communicate = edge_tts.Communicate(texto, voz_id, rate=velocidad)
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
    print("🎤 PRUEBA DE VOCES - Catalina y Elena con Velocidad Ajustada")
    print("="*70)
    
    # Textos de prueba
    textos_prueba = [
        "¡Hola padrino! Bienvenido al strim. ¿Sabías que los videojuegos retro están de moda?",
        "Aquí tienes un dato curioso: Minecraft fue creado en solo seis días por Notch.",
        "¿Qué opinas sobre el nuevo parche de League of Legends? Los cambios están interesantes."
    ]
    
    
    # Configuraciones para probar
    configuraciones = [
        # Catalina (Colombia)
        ("Catalina - Velocidad Normal (0%)", "es-CO-SalomeNeural", "+0%"),
        ("Catalina - Velocidad Rápida (+25%)", "es-CO-SalomeNeural", "+25%"),
        ("Catalina - Velocidad Muy Rápida (+40%)", "es-CO-SalomeNeural", "+40%"),
        
        # Pausa entre voces
        None,

        ("Dalia - Velocidad Normal (0%)", "es-MX-DaliaNeural", "+0%"),
        ("Dalia - Velocidad Rápida (+25%)", "es-MX-DaliaNeural", "+25%"),
        ("Dalia - Velocidad Muy Rápida (+40%)", "es-MX-DaliaNeural", "+40%"),

        None,
        
        # Elena (Argentina)
        ("Elena - Velocidad Normal (0%)", "es-AR-ElenaNeural", "+0%"),
        ("Elena - Velocidad Rápida (+25%)", "es-AR-ElenaNeural", "+25%"),
        ("Elena - Velocidad Muy Rápida (+40%)", "es-AR-ElenaNeural", "+40%"),
    ]
    
    print("\n📝 Se probarán diferentes velocidades con frases de ejemplo.")
    print("   Escucha cuál suena más natural para tu stream.\n")
    
    input("Presiona Enter para comenzar...")
    
    for config in configuraciones:
        if config is None:
            print("\n" + "-"*70)
            print("Cambiando a siguiente voz...")
            print("-"*70)
            await asyncio.sleep(1)
            continue
        
        nombre, voz_id, velocidad = config
        texto = textos_prueba[0]  # Usar la primera frase
        
        await probar_voz(nombre, voz_id, velocidad, texto)
        await asyncio.sleep(1.5)  # Pausa entre pruebas
    
    print("\n" + "="*70)
    print("✅ Prueba completada!")
    print("\n💡 Recomendaciones:")
    print("   - Para Catalina: +25% a +30% suena natural y dinámico")
    print("   - Para Elena: +20% a +25% suena bien con el acento argentino")
    print("\n📝 Para cambiar en el bot:")
    print("   1. Edita bot_unificado.py")
    print("   2. Cambia VOZ_EDGE_TTS = 'es-CO-SalomeNeural' (Catalina)")
    print("      O VOZ_EDGE_TTS = 'es-AR-ElenaNeural' (Elena)")
    print("   3. Ajusta VOZ_VELOCIDAD = '+25%' (o el % que prefieras)")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️ Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
