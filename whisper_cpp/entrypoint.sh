#!/bin/bash
set -e

WHISPER_SRC="/app/whisper.cpp" # путь к проекту, где лежат исходники
BUILD_DIR="$WHISPER_SRC/build" # папка, в которой будут лежать бинарники сборки
MODEL_DIR="/models" # папка, где хранятся скаченные модели
MODEL_NAME="${WHISPER_MODEL:-large-v3-turbo}"
MODEL_FILE="$MODEL_DIR/ggml-$MODEL_NAME.bin" # итоговый путь до модели

WHISPER_HOST="${WHISPER_HOST:-0.0.0.0}"
WHISPER_PORT="${WHISPER_PORT:-8080}" # порт для веб интерфейса

# сборка whisper.cpp, если бинарник отсутствует
if [ ! -f "$BUILD_DIR/bin/whisper-server" ]; then
    echo "🔨 Сборка whisper.cpp (первый запуск, может занять несколько минут)..."
    cd "$WHISPER_SRC"
    mkdir -p "$BUILD_DIR"
    cd "$BUILD_DIR"
    cmake .. -DGGML_HIP=1 -DAMDGPU_TARGETS="gfx1102"
    make -j$(nproc)
    echo "✅ Сборка завершена."
else
    echo "✅ Бинарник уже собран."
fi

# скачивание модели, если отсутствует через скрипт в репозитории
if [ ! -f "$MODEL_FILE" ]; then
    echo "🔨 Модель $MODEL_NAME не найдена. Скачиваем..."
    wget -L -O "$MODEL_FILE" "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-$MODEL_NAME.bin"
    echo "✅ Модель скачана."
else
    echo "✅ Модель $MODEL_NAME уже есть."
fi

# запуск сервера
echo "======== В КОСМОС!!!! ======== Запуск whisper-server на $WHISPER_HOST:$WHISPER_PORT"
exec "$BUILD_DIR/bin/whisper-server" -m "$MODEL_FILE" --host "$WHISPER_HOST" --port "$WHISPER_PORT" --language ru