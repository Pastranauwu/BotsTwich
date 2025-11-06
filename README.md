# 🎮 Bot de Twitch con Personalidades IA

Bot interactivo para Twitch con **3 personalidades únicas** que usan voces neuronales de Azure y la API de DeepSeek.

## 🌟 Las Chicas del Bot

### 😈 Eris (Colombia)
- **Personalidad**: Traviesa y divertida, ama el caos controlado
- **Voz**: `es-CO-SalomeNeural` (Colombiana natural)
- **Velocidad**: +30% (rápida y juguetona)
- **Expresiones**: "¡Qué desastre!", "Caos puro", "Esto se pone interesante"

### ✨ Sylph (Argentina)
- **Personalidad**: Elegante y misteriosa con toque mágico
- **Voz**: `es-AR-ElenaNeural` (Argentina sofisticada)
- **Velocidad**: +25% (pausada y reflexiva)
- **Expresiones**: "Interesante...", "La magia de esto es...", "Qué fascinante"

### 🌟 Roxy (México)
- **Personalidad**: Enérgica, amigable y súper positiva
- **Voz**: `es-MX-DaliaNeural` (Mexicana alegre)
- **Velocidad**: +28% (enérgica y motivadora)
- **Expresiones**: "¡Qué padre!", "¡Increíble!", "¡Dale, dale!"

**Cambian automáticamente cada 5 ciclos** para mantener el stream dinámico.

## 🎙️ Tecnología de Voces

### Azure Speech Services (Oficial de Microsoft)
- ✅ **5 MILLONES de caracteres GRATIS al mes**
- ✅ Voces neuronales de **MÁXIMA CALIDAD**
- ✅ Oficial y estable (sin errores 401)
- ✅ Mismo motor que Edge TTS pero con API oficial

**Costo real**: $0 para streamers (25-50 streams completos gratis/mes)

## 🚀 Instalación Rápida

### 1. Instalar dependencias
```bash
pip install -r requeriments.txt
```

**Linux (Arch)**: Si tienes restricciones de pip:
```bash
pip install --user -r requeriments.txt
```

### 2. Configurar API Keys

Crea un archivo `.env` basado en `.env.example`:

```env
# DeepSeek (IA conversacional)
DEEPSEEK_API_KEY=sk-tu-key-aqui

# Azure Speech Services (Voces neuronales)
AZURE_SPEECH_KEY=tu-azure-key
AZURE_REGION=eastus
```

**Obtén tus keys**:
- **DeepSeek**: https://platform.deepseek.com (gratis, sin tarjeta)
- **Azure**: https://portal.azure.com (tier F0 gratis)

📖 **Guía paso a paso de Azure**: [GUIA_AZURE.md](GUIA_AZURE.md)

### 3. Probar las personalidades
```bash
python3 test_personalidades.py
```

Escucharás a Eris 😈, Sylph ✨ y Roxy 🌟 presentándose.

### 4. Ejecutar el bot completo
```bash
python3 bot_unificado.py
```

## 🌟 Características

- **🎭 3 Personalidades Únicas**: Eris, Sylph y Roxy con voces y estilos distintos
- **🎙️ Voces Neuronales Premium**: Azure Speech Services (5M caracteres gratis/mes)
- **🤖 IA Conversacional**: DeepSeek para respuestas inteligentes en español
- **🎤 Reconocimiento de Voz**: Escucha y responde a tu micrófono
- **❓ Preguntas Automáticas**: Genera contenido sobre videojuegos, tecnología, anime
- **🔄 Rotación Automática**: Cambia de personalidad cada 5 ciclos
- **💬 Adaptación Fonética**: Palabras en inglés suenan naturales en español
- **🎯 Sistema Robusto**: Manejo inteligente de errores y reintentos

## 📋 Requisitos

- Python 3.8+
- Micrófono (para modo conversación)
- Conexión a internet
- Cuenta gratuita de DeepSeek
- Cuenta gratuita de Azure (tier F0 - 5M caracteres/mes)

## ⚙️ Configuración

### Intervalos y tiempos

Edita `bot_unificado.py`:

```python
# Tiempos (en segundos)
INTERVALO_PREGUNTA_AUTOMATICA = 240  # Preguntas cada 4 min
INTERVALO_ESCUCHAR_MICROFONO = 120   # Escuchar cada 2 min
PROBABILIDAD_MICROFONO = 0.3  # 30% micrófono, 70% preguntas
```

### Personalizar personalidades

Edita el diccionario `PERSONALIDADES` para:
- Cambiar velocidad de voz
- Modificar rasgos de personalidad
- Agregar nuevas expresiones

📖 **Guía completa**: [PERSONALIDADES.md](PERSONALIDADES.md)

## 🎯 Cómo Funciona

1. **Inicio**: El bot elige una personalidad aleatoria y saluda
2. **Ciclo Continuo**:
   - **70% del tiempo**: Genera preguntas/comentarios con la personalidad actual
   - **30% del tiempo**: Escucha tu micrófono para conversar
   - **Cada 5 ciclos**: Cambia de personalidad automáticamente
3. **Cuando escucha**:
   - Emite un "beep"
   - Graba tu voz (~10 segundos)
   - Transcribe a texto
   - Envía a DeepSeek con contexto de personalidad
   - Responde con voz neural de Azure

## 📁 Archivos del Proyecto

```
BotsTwich/
├── bot_unificado.py         # 🎯 Bot principal con Azure Speech
├── test_personalidades.py   # 🧪 Prueba las 3 personalidades
├── GUIA_AZURE.md           # 📖 Guía configuración Azure (paso a paso)
├── PERSONALIDADES.md       # 🎭 Guía del sistema de personalidades
├── CONFIGURACION_VOZ.md    # 🎙️ Guía de voces y fonética
├── requeriments.txt        # 📦 Dependencias
├── .env                    # 🔐 Tus API keys (no subir a git)
├── .env.example            # 📝 Plantilla de configuración
└── README.md               # 📄 Este archivo
```

## 🔧 Solución de Problemas

### ❌ Error: "Azure Speech Services no configurado"
1. Verifica que tu `.env` tenga `AZURE_SPEECH_KEY` y `AZURE_REGION`
2. Consulta [GUIA_AZURE.md](GUIA_AZURE.md) para obtener tus credenciales

### ❌ Error: "Invalid subscription key"
- Verifica que copiaste la key completa sin espacios
- La región debe estar en minúsculas: `eastus`, `westeurope`, etc.

### ❌ Error 401 (API DeepSeek)
```bash
cat .env
# Debe mostrar: DEEPSEEK_API_KEY=sk-xxxxxx
```

### ❌ No se escucha la voz
**Linux**:
```bash
sudo apt-get install libsdl2-mixer-2.0-0
```

**Mac**:
```bash
brew install sdl2_mixer
```

### ❌ Error con el micrófono
```bash
# Linux
sudo apt-get install portaudio19-dev python3-pyaudio

# Mac  
brew install portaudio

# Luego
pip install pyaudio
```

### ❌ Error: "Module not found: azure"
```bash
pip install azure-cognitiveservices-speech
```

## 📊 Comparación: Edge TTS vs Azure Speech

| Aspecto | Edge TTS (Gratis) | Azure Speech (F0) |
|---------|-------------------|-------------------|
| Calidad | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Voces | Mismas | Mismas |
| Estabilidad | ❌ Error 401 | ✅ Oficial |
| Límite mensual | Bloqueado | 5M caracteres |
| Configuración | Simple | Simple |
| Costo | $0 | $0 (tier gratuito) |
| **Recomendado** | ❌ No funciona | ✅ Usar este |

## 💰 Costos de Azure Speech

### Tier Gratuito (F0)
- **5,000,000 caracteres/mes** GRATIS
- **20 solicitudes simultáneas**
- Todas las voces neuronales incluidas

### ¿Cuánto es 5 millones de caracteres?
- 1 respuesta del bot ≈ 100 caracteres
- **50,000 respuestas gratis al mes**
- Stream de 8 horas ≈ 500 respuestas
- **Puedes streamear 100 días al mes** sin pagar

### Tier de pago (solo si superas el límite gratuito)
- $16 USD por cada millón adicional
- Recibes alertas antes de ser cobrado
- Puedes establecer límites de gasto

## 🎨 Características Avanzadas

### Adaptación Fonética Automática

El bot convierte palabras en inglés a fonética española:
- "Minecraft" → "Maincraf"
- "League of Legends" → "Lig of Leyends"
- "streamer" → "estrimer"
- "Twitch" → "Tuich"

Ver lista completa: [CONFIGURACION_VOZ.md](CONFIGURACION_VOZ.md)

### Sistema de Personalidades

Cada personalidad tiene:
- Prompt system único para DeepSeek
- Voz característica con acento regional
- Velocidad de habla personalizada
- Expresiones y estilo de comunicación propios

Cambio automático cada 5 ciclos para variedad.

## 📚 Documentación Completa

- 📖 [GUIA_AZURE.md](GUIA_AZURE.md) - Configuración Azure paso a paso
- 🎭 [PERSONALIDADES.md](PERSONALIDADES.md) - Sistema de personalidades
- 🎙️ [CONFIGURACION_VOZ.md](CONFIGURACION_VOZ.md) - Voces y fonética

## 🤝 Contribuir

¿Ideas para nuevas personalidades? ¿Mejoras al bot?
¡Abre un issue o pull request!

## 📝 Licencia

MIT License - Úsalo libremente para tus streams

---

**Hecho con ❤️ para streamers de Twitch**
