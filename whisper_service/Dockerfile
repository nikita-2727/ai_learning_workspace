FROM rocm/pytorch:latest

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/root/.cache/huggingface

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

# Копируем файл патча С ХОСТА В КОНТЕЙНЕР (контекст сборки = ./whisper_service)
COPY patch_asr.py /tmp/patch_asr.py

# библиотека для работы с кастомной моделью чтобы прочитать токенизатор
RUN pdm add "transformers<4.40.0" protobuf 

# Устанавливаем зависимости через PDM 
RUN pdm install --no-editable --prod --no-self

# Это заставит его использовать pure-Python токенизатор, который ИГНОРИРУЕТ сломанный tokenizer.json
RUN sed -i 's/AutoTokenizer\.from_pretrained(self\.config\.model_name)/AutoTokenizer.from_pretrained(self.config.model_name, use_fast=False)/g' /app/insanely_fast_whisper_rocm/core/asr_backend.py

# Патчим transformers в .venv PDM
RUN /app/.venv/bin/python -c "import os; config_file='/app/.venv/lib/python3.10/site-packages/transformers/configuration_utils.py'; lines=open(config_file,'r').readlines(); [lines.__setitem__(i, line.replace('return json.dumps(config_dict, indent=2, sort_keys=True)', 'return json.dumps(config_dict, indent=2, sort_keys=True, default=str)')) for i, line in enumerate(lines) if 'return json.dumps(config_dict, indent=2, sort_keys=True)' in line]; open(config_file,'w').writelines(lines); print('SUCCESS: transformers patched')"

# Применяем патч очистки тегов
RUN /app/.venv/bin/python /tmp/patch_asr.py


# Открываем порты
EXPOSE 7860 8000

# Запускаем WebUI через pdm run (он использует системный Python)
CMD ["pdm", "run", "python", "-m", "insanely_fast_whisper_rocm.webui"]

# CMD ["pdm", "run", "python", "-m", "insanely_fast_whisper_rocm.api"]