from pathlib import Path
from datasets import load_dataset, Audio

# Определяем папку, где лежит этот скрипт
BASE_DIR = "/workspace/datasets/oil_and_gas_ready_dataset"

# Загружаем датасет, пока считая колонку audio обычной строкой
dataset = load_dataset(
    "json",
    data_files={
        "train": str(BASE_DIR / "train" / "metadata.jsonl"),
        "validation": str(BASE_DIR / "validation" / "metadata.jsonl"),
        "test": str(BASE_DIR / "test" / "metadata.jsonl")
    }
)

# исправляет пути на абсолютные
def fix_audio_paths(example, split_name):
    # example["audio"] сейчас это строка, "audio/train_0.mp3"
    # получаем имя файла
    filename = str(example["audio"]).split("/")[-1]
    
    # Собираем абсолютный путь: /путь/к/проекту/train/audio/train_0.mp3
    correct_absolute_path = str(BASE_DIR / split_name / "audio" / filename)
    
    example["audio"] = correct_absolute_path
    return example

# Применяем исправление путей к каждому сплиту
print("Исправляю пути к аудиофайлам...")
dataset["train"] = dataset["train"].map(lambda x: fix_audio_paths(x, "train"))
dataset["validation"] = dataset["validation"].map(lambda x: fix_audio_paths(x, "validation"))
dataset["test"] = dataset["test"].map(lambda x: fix_audio_paths(x, "test"))

# конвертируем в тип Audio
print("Конвертирую колонку audio в формат Audio...")
dataset = dataset.cast_column("audio", Audio(sampling_rate=16000))

# проверка
print("Проверка первого элемента train:", dataset["train"][0]["audio"])
print(f"Примеров в train: {len(dataset['train'])}")

# загрузка на Hugging Face
print("Начинаю загрузку на Hugging Face...")
dataset.push_to_hub("N07P/oil_and_gas_speech")

print("Готово! Parquet-файлы созданы и загружены.")