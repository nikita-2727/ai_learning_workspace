FROM rocm/pytorch:latest

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем PDM глобально 
RUN pip install --no-cache-dir pdm

# Клонируем репозиторий insanely-fast-whisper-rocm ( проект и зависимости будут  лежать в app/ )
ARG REPO_URL=https://github.com/beecave-homelab/insanely-fast-whisper-rocm.git
ARG BRANCH=main
RUN git clone --depth 1 --branch ${BRANCH} ${REPO_URL} /app

# Автоматически исправляем баг в коде: заменяем dtype= на правильный torch_dtype=
RUN sed -i 's/dtype=torch\.float16/torch_dtype=torch.float16/g' /app/insanely_fast_whisper_rocm/core/asr_backend.py
RUN sed -i 's/dtype=torch\.bfloat16/torch_dtype=torch.bfloat16/g' /app/insanely_fast_whisper_rocm/core/asr_backend.py


# Устанавливаем зависимости через PDM 
RUN pdm install --no-editable --prod --no-self

# Открываем порты
EXPOSE 7860 8000

# Запускаем WebUI через pdm run (он использует системный Python)
CMD ["pdm", "run", "python", "-m", "insanely_fast_whisper_rocm.webui"]