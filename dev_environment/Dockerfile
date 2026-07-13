FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y \
    ffmpeg \ 
    unzip \
    git \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем все библиотеки для дообучения и работы с данными
RUN pip install --no-cache-dir \
    yt-dlp \
    tqdm \
    librosa \
    soundfile \
    git+https://github.com/i4Ds/whisper-prep.git \
    prompt_toolkit \
    pygame

# Установка Deno для решения n-сигнатуры YouTube
COPY deno_binary/deno-x86_64-unknown-linux-gnu/deno /usr/local/bin/deno
RUN chmod +x /usr/local/bin/deno

CMD ["/bin/bash"]