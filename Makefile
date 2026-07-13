SERVICE_DEFAULT := whisper-default-cli

# работа с докер контейнерами
up:
	docker compose up -d $(SERVICE_DEFAULT)

stop:
	docker compose stop $(SERVICE_DEFAULT)

logs:
	docker compose logs -f $(SERVICE_DEFAULT)

restart: stop up



# транскрибация
whisper_cli: # не поддерживает probability и confidence
	./whisper_service/start_cli.sh

whisper_api:
	./whisper_service/start_api.sh

whisper_cpp: # полный вывод
	./whisper_cpp/start_api.sh



# скачивание аудио
u ?= https://youtu.be/
o ?= workspace/audio
f ?= wav
p ?= false
q ?= false

download:
	docker exec -it development \
	python scripts/download_audio.py $(u) -o $(o) -f $(f) $(if $(filter true,$(p)),-p,) $(if $(filter true,$(q)),-q,) 

download-list:
	@echo "Скачивание из файла audio_source.txt"
	@while read -r url; do \
		docker exec development \
		python scripts/download_audio.py "$$url" -o $(o) -f $(f); \
	done < workspace/metadata/audio_source.txt

download-help:
	docker exec -it development \
	python scripts/download_audio.py -h



# разбиение на чанки, приведение текста к формату для обучения с таймкодами 
wav=/workspace/audio
srt=/workspace/transcripts_srt
out=/workspace/datasets

whisper-prep:
	docker exec -it development \
	python scripts/temp_dataset.py $(wav) $(srt) -o $(out)

whisper-prep-help:
	docker exec -it development \
	python scripts/temp_dataset.py -h



# распознавание типа чанка и стратификация, приведение к формату hf
prepare-dataset:
	docker exec -it development \
	python scripts/prepare_dataset.py

# получает общий размер метаданных и файлов в байтах
dataset-info:
	docker exec -it development \
	python scripts/dataset_info.py

# запускает скрипт для проверки 20% чанков из train
dataset-validate:
	docker exec -it development \
	python scripts/fix_problem_chunks.py



# загружает модель в hf
dataset-upload:
	docker exec -it development \
	huggingface-cli upload your-username/oil_and_gas_speech /workspace/datasets/oil_and_gas_ready_dataset \
	--repo-type dataset --commit-message "Initial dataset upload"

# обновляет определенные файлы в модели на hf
new_path=new_metadata.jsonl

dataset-edit:
	huggingface-cli upload your-username/oil_and_gas_speech $(new_path) train/metadata.jsonl --repo-type dataset


# не зависимо от папок с таким же именем, цели будут выполняться
.PHONY: up stop logs restart whisper_cli whisper_api whisper_cpp download download-list download-help whisper-prep whisper-prep-help prepare-dataset