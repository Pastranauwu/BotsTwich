#!/bin/bash

# Script de inicio rápido para el Bot de Twitch

echo "🎮 Bot de Twitch - DeepSeek Edition 🎮"
echo "======================================"
echo ""

# Verificar si existe .env
if [ ! -f .env ]; then
    echo "⚠️  No se encontró archivo .env"
    echo "📝 Creando .env desde .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANTE: Edita el archivo .env y agrega tu API key de DeepSeek"
    echo "   Puedes obtenerla en: https://platform.deepseek.com/"
    echo ""
    read -p "Presiona Enter después de configurar tu API key en .env..."
fi

# Verificar si las dependencias están instaladas
echo "🔍 Verificando dependencias..."
if ! python3 -c "import speech_recognition, requests, pyttsx3, dotenv" 2>/dev/null; then
    echo "📦 Instalando dependencias..."
    pip install -r requeriments.txt
else
    echo "✅ Dependencias instaladas"
fi

echo ""
echo "🚀 Iniciando bot..."
echo "   Presiona Ctrl+C para detener"
echo ""

# Ejecutar el bot
python3 bot_unificado.py
