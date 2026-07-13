import os
import subprocess
import sys
import argparse
import yaml


def run_whisper_prep(audio_dir: str, srt_dir: str, output_dir: str = "/workspace/datasets"):
    """
    Запускает whisper-prep для обработки пары папок: audio + srt.
    По итогу получает папку с нарезанными чанками и готовым jsonl
    Имена файлов .wav и .srt должны быть одинаковы
    """
    # Проверяем, что папки существуют
    if not os.path.isdir(audio_dir):
        print(f"папка с аудио не найдена: {audio_dir}")
        sys.exit(1)
    if not os.path.isdir(srt_dir):
        print(f"папка с SRT не найдена: {srt_dir}")
        sys.exit(1)

    # Создаём выходную папку, если её нет
    os.makedirs(output_dir, exist_ok=True)

    # Формируем конфиг для передачи в whisper-prep
    config = {
        "dataset_name": "whisper_prep_dataset",
        "split_name": "train",
        "language": "ru",
        "source_audio_dir": audio_dir,
        "source_transcript_dir": srt_dir,
        "out_folder_base": output_dir,
        "format": "jsonl",
        "num_proc": 4
    }

    config_path = "scripts/configs/whisper_prep.yaml"
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True)

    # команда для запуска
    cmd = ["whisper_prep", "-c", config_path]

    print(f"====== В КОСМОС!!! ======= Запуск whisper-prep...")
    print(f"   Аудио: {audio_dir}")
    print(f"   SRT:   {srt_dir}")
    print(f"   Выход: {output_dir}")

    try:
        subprocess.run(cmd, check=True)
        print(f"======= IT WORKED!!! ======= Результат в папке: {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"======= BIG MISTAKE!!! ======= Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Подготавливает датасет из файлов .wav и .srt",
        epilog="Пример: python prepare_dataset.py "
    )
    
    parser.add_argument(
        "wav",
        help="Папка c аудиофайлами .wav"
    )
    parser.add_argument(
        "srt",
        help="Папка с транскрипциями .srt"
    )
    parser.add_argument(
        "-o", "--output-dir",
        default="/workspace/prepare_dataset",
        help="Выходная папка"
    )

    args = parser.parse_args()

    run_whisper_prep(args.wav, args.srt, args.output_dir)