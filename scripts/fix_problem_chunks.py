import json
import csv
import os
import pygame
import threading
from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings

# === НАСТРОЙКИ ===
CSV_FILE = "/workspace/metadata/chunk_manual_verification.csv"  # ваш CSV с проблемными чанками
JSONL_FILE = "/workspace/metadata/originale_jsonl/train.jsonl"  # исходный JSONL, который нужно поправить
OUTPUT_JSONL = "/workspace/metadata/validate_jsonl/train.jsonl"

pygame.mixer.init()

def play_audio(audio_path, stop_event):
    """Фоновое воспроизведение аудио (останавливается при stop_event.set())."""
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        if stop_event.is_set():
            pygame.mixer.music.stop()
            break
        pygame.time.Clock().tick(10)

def editor_with_playback(initial_text, audio_path):
    """Редактор prompt_toolkit с фоновым воспроизведением аудио и повтором по Ctrl+R."""
    bindings = KeyBindings()
    stop_flag = threading.Event()
    play_thread = None

    def start_playback():
        nonlocal play_thread, stop_flag
        # Останавливаем предыдущее воспроизведение, если оно ещё идёт
        if play_thread and play_thread.is_alive():
            stop_flag.set()
            play_thread.join(timeout=0.5)
        stop_flag.clear()
        play_thread = threading.Thread(target=play_audio, args=(audio_path, stop_flag))
        play_thread.daemon = True
        play_thread.start()

    @bindings.add('c-r')  # Ctrl+R – повтор аудио
    def replay(event):
        start_playback()

    # Запускаем первое воспроизведение
    start_playback()

    # Запускаем редактор (многострочный, чтобы видеть весь текст)
    new_text = prompt(
        "Редактируйте текст (Ctrl+R – повторить аудио, Enter – сохранить): ",
        default=initial_text,
        key_bindings=bindings,
        multiline=True  # удобнее для длинных транскрипций
    )

    # Останавливаем воспроизведение после выхода из редактора
    if play_thread and play_thread.is_alive():
        stop_flag.set()
        play_thread.join(timeout=0.5)

    return new_text



def main():
    # Читаем JSONL метаданные
    with open(JSONL_FILE, 'r', encoding='utf-8') as f:
        records = [json.loads(line) for line in f]

    # создаем мапу, где ключ - индекс для быстрого поиска
    index_to_record = {rec["index"]: rec for rec in records}

    # Читаем CSV с проблемными чанками
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        problems = list(csv.DictReader(f))

    print(f"Найдено {len(problems)} чанков для проверки.")

    for row in problems:
        # берем индекс, абсолютный путь до аудио и текст из CSV
        idx = int(row["index"])
        audio_path = row["audio"]
        orig_text = row["text"]

        # получаем запись в jsonl по индексу
        rec = index_to_record.get(idx)
        if rec is None:
            print(f"==== MISTAKE!!! ==== Запись index={idx} не найдена в JSONL, пропускаем.")
            continue

        print("\n" + "="*60)
        print(f"Чанк index={idx}, тип={row['type']}, avg_prob={row['avg_prob']}")
        print("Текущий текст:")
        print(orig_text)

        if not os.path.exists(audio_path):
            print(f"==== MISTAKE!!! ==== Аудиофайл не найден: {audio_path}")
            # Если аудио нет – просто даём отредактировать текст в обычном режиме
            new_text = prompt("Отредактируйте текст (Enter для сохранения как есть): ", default=orig_text)
        else:
            # Запускаем редактор с параллельным воспроизведением
            new_text = editor_with_playback(orig_text, audio_path)

        rec["text"] = ' '.join(new_text.split())  # удаляем лишние пробелы
        print("✅ Текст сохранён.")

    # Сохраняем JSONL
    with open(OUTPUT_JSONL, 'w', encoding='utf-8') as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')

    print(f"\nГотово! Исправленный файл: {OUTPUT_JSONL}")

if __name__ == "__main__":
    main()