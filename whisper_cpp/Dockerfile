FROM rocm/dev-ubuntu-22.04:6.3-complete

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential cmake git wget \
    && rm -rf /var/lib/apt/lists/*

# появляется папка app/whisper.cpp c исходниками
RUN git clone https://github.com/ggerganov/whisper.cpp.git

# Копируем entrypoint-скрипт
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]