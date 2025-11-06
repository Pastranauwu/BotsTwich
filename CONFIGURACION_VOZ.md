# 🎙️ Configuración de Voces - Bot de Twitch

## Voces Seleccionadas

El bot está configurado para usar estas 3 voces naturales con velocidad +25% a +30%:

### 1. Catalina (Colombia) - Principal ⭐
```python
VOZ_EDGE_TTS = "es-CO-SalomeNeural"
VOZ_VELOCIDAD = "+30%"
```
- Acento colombiano
- Muy clara y natural
- Perfecta para gaming

### 2. Elena (Argentina)
```python
VOZ_EDGE_TTS = "es-AR-ElenaNeural"
VOZ_VELOCIDAD = "+25%"
```
- Acento argentino
- Cálida y amigable
- Ideal para contenido variado

### 3. Dalia (México)
```python
VOZ_EDGE_TTS = "es-MX-DaliaNeural"
VOZ_VELOCIDAD = "+28%"
```
- Acento mexicano
- Energética
- Excelente para streams dinámicos

## 🌍 Adaptación Fonética Español

El bot está configurado para que DeepSeek adapte palabras en inglés a su pronunciación fonética en español, para que la voz suene natural.

### Ejemplos de Adaptación

| Palabra Original | Fonética en Español | Uso |
|-----------------|---------------------|-----|
| **Videojuegos** |
| Minecraft | Maincraf | "En Maincraf puedes construir lo que quieras" |
| Fortnite | Fortnait | "El Fortnait tiene un nuevo modo de juego" |
| League of Legends | Lig of Leyends | "El Lig of Leyends tiene nuevo parche" |
| GTA | yi ti ei | "El yi ti ei cinco sigue siendo popular" |
| Call of Duty | Col of Diuti | "El nuevo Col of Diuti sale este año" |
| **Términos Gaming** |
| streamer | estrimer | "Ese estrimer es muy bueno" |
| gameplay | geimplei | "El geimplei es súper fluido" |
| bug | bag | "Encontré un bag en el juego" |
| patch | pach | "Salió un nuevo pach de actualización" |
| nerf | nerf | "Le hicieron nerf a esa arma" |
| buff | baf | "Le dieron un baf al personaje" |
| **Plataformas** |
| Discord | Díscord | "Únete al Díscord del canal" |
| YouTube | Yutiub | "Súbelo a Yutiub después" |
| Twitch | Tuich | "Este Tuich está en vivo" |
| Steam | Estim | "Lo compré en Estim" |
| **Tecnología** |
| mouse | maus | "Necesito un maus nuevo" |
| keyboard | quibord | "Mi quibord tiene luces RGB" |
| headset | jedset | "Compré un jedset gamer" |
| PC | pi si | "Mi pi si corre todo a 60 FPS" |

## 💡 Cómo Funciona

El bot usa instrucciones específicas en el prompt del sistema para que DeepSeek:

1. ✅ **Responda siempre en español**
2. ✅ **Adapte palabras en inglés fonéticamente**
3. ✅ **Mantenga nombres propios reconocibles**
4. ✅ **Use lenguaje natural para la voz**

### Ejemplo de Conversación

**Usuario**: "¿Qué opinas del nuevo parche de League?"

**Bot (texto)**: "¡El nuevo pach del Lig of Leyends está genial! Balancearon varios campeones y agregaron un nuevo estrimer de dragones. ¿Ya lo probaste?"

**Bot (voz)**: *Se escucha natural en español, sin trabarse en palabras en inglés*

## 🔧 Cambiar Voz Rápidamente

Edita `bot_unificado.py` en las líneas 21-22:

```python
# Para Catalina (Colombia) - Recomendada
VOZ_EDGE_TTS = "es-CO-SalomeNeural"
VOZ_VELOCIDAD = "+30%"

# Para Elena (Argentina)
VOZ_EDGE_TTS = "es-AR-ElenaNeural"
VOZ_VELOCIDAD = "+25%"

# Para Dalia (México)
VOZ_EDGE_TTS = "es-MX-DaliaNeural"
VOZ_VELOCIDAD = "+28%"
```

## 🎯 Ajustar Velocidad

Puedes experimentar con diferentes velocidades:

```python
VOZ_VELOCIDAD = "+20%"  # Más pausada
VOZ_VELOCIDAD = "+25%"  # Equilibrada
VOZ_VELOCIDAD = "+30%"  # Dinámica (recomendada)
VOZ_VELOCIDAD = "+35%"  # Muy rápida
VOZ_VELOCIDAD = "+40%"  # Hiperactiva
```

**Recomendación**: Entre +25% y +30% es el punto ideal para sonar natural sin ser robótica.

## 📝 Notas Importantes

1. **Internet requerido**: Edge TTS necesita conexión para generar el audio
2. **Primera vez más lento**: El primer audio puede tardar un poco más
3. **Calidad profesional**: Las voces son las mismas que usa Microsoft Azure
4. **Sin límites**: Gratis y sin restricciones de uso

## 🧪 Probar Configuración

```bash
# Probar las 3 voces con diferentes velocidades
python3 prueba_voz.py

# Probar el bot completo (3 ciclos rápidos)
python3 test_bot.py

# Ejecutar bot completo
python3 bot_unificado.py
```

---

**Configurado para sonar natural en español** 🎙️🇪🇸
