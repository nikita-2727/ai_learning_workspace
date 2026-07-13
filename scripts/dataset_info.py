import os
from pathlib import Path

"""
считает download_size и dataset_size для dataset_info.json
"""

OUTPUT_DIR = "/workspace/datasets/oil_and_gas_ready_dataset"   

def get_dir_size(path):
    """Рекурсивно подсчитывает суммарный размер файлов в директории."""
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp):
                total += os.path.getsize(fp)
    return total


def main():
    # подсчет download_size и dataset_size
    print(f"\n ==== ПОДСЧЕТ ДОПОЛНИТЕЛЬНЫХ ДАННЫХ ====")

    dataset_dir = Path(OUTPUT_DIR)
    # Размер всех аудио (обычно = download_size)
    download_size = get_dir_size(dataset_dir / "train" / "audio") + \
                    get_dir_size(dataset_dir / "validation" / "audio") + \
                    get_dir_size(dataset_dir / "test" / "audio")

    # Размер всех metadata.jsonl + dataset_info.json + README.md (можно добавить любой текстовый размер)
    metadata_files = [
        dataset_dir / "train" / "metadata.jsonl",
        dataset_dir / "validation" / "metadata.jsonl",
        dataset_dir / "test" / "metadata.jsonl",
        dataset_dir / "dataset_info.json"
    ]
    dataset_size = sum(os.path.getsize(f) for f in metadata_files if f.exists())

    print(f"download_size: {download_size} байт")
    print(f"dataset_size: {dataset_size} байт")


if __name__ == "__main__":
    main()