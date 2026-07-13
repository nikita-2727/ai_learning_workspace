import os
import argparse
import sys
import yt_dlp

def download_audio(url, output_dir="workspace/audio", format="wav", playlist=False, quiet=False):
    """
    Скачивает аудио с YouTube.
    
    параметры:
        url (str): Ссылка на видео или плейлист
        output_dir (str): Папка для сохранения
        format (str): Аудиоформат ('wav', 'mp3', 'm4a')
        playlist (bool): Скачивать весь плейлист
        quiet (bool): Подавить вывод прогресса
    """
    # если нет папки, создаем
    os.makedirs(output_dir, exist_ok=True)

    # deno не может загрузить JavaScript‑файл плеера через прокси - SSL handshake timeout
    # ВАЖНО: прокси для deno и других подпроцессов
    # перенаправляем deno на наш прокси через переменные окружения
    proxy_url = 'socks5h://192.168.1.38:10808'
    os.environ['HTTP_PROXY'] = proxy_url
    os.environ['HTTPS_PROXY'] = proxy_url
    os.environ['ALL_PROXY'] = proxy_url
    
    # настройки
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio', # используем конкретный аудиоформат, который доступен без n-сигнатуры
        'postprocessors': [{ # конвертируем в нужный формат
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,
            'preferredquality': '0',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': quiet,
        'no_warnings': quiet,
        'ignoreerrors': True,  # продолжать при ошибках в плейлисте
        'force_ipv4': True, # решаем проблему с таймаутами
        'proxy': proxy_url,
        'cookiefile': '/workspace/metadata/cookies.txt',
        # используем Deno для обхода n-сигнатуры YouTube
        'extractor_args': {
            'youtube': {
                'js_runtimes': ['deno'],
            }
        },
        'remote_components': ['ejs:github'],

        'retries': 10, # количество попыток при ошибках сети
        'fragment_retries': 10, # для DASH/HLS
        'socket_timeout': 30, # таймаут сокета в секундах
        'no_part': True, # не оставлять .part файлы при ошибке
    }
    
    # Для одного видео останавливаем обработтку на первом
    if not playlist:
        ydl_opts['playlistend'] = 1 


    downloaded_files = []
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Загрузка: {url}")

            # получаем информацию
            info = ydl.extract_info(url, download=True)

            # плейлист
            if 'entries' in info:
                for entry in info['entries']:
                    if entry is not None:
                        # Определяем имя файла по шаблону
                        filename = ydl.prepare_filename(entry)
                        downloaded_files.append(filename)
                        print(f"ОК ---- {filename}")
                        
            # Одиночное видео
            else:
                filename = ydl.prepare_filename(info)
                downloaded_files.append(filename)
                print(f"ОК ---- {filename}")
            

            print(f"Загрузка завершена. Сохранено файлов: {len(downloaded_files)}")
            for file in downloaded_files: print(file)
            
    except Exception as e:
        print(f"ОШИБКА: {e}", file=sys.stderr)



def main():
    parser = argparse.ArgumentParser(
        description="Скачивание аудио с YouTube",
        epilog="Пример: python download_audio.py https://youtu.be/... -o my_audio -f mp3"
    )
    
    parser.add_argument(
        "url",
        help="Ссылка на видео или плейлист YouTube"
    )
    parser.add_argument(
        "-o", "--output-dir",
        default="audio",
        help="Папка для сохранения (по умолчанию: audio)"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["wav", "mp3", "m4a", "flac", "aac"],
        default="wav",
        help="Аудиоформат (по умолчанию: wav)"
    )
    parser.add_argument(
        "-p", "--playlist",
        action="store_true",
        help="Скачать весь плейлист (иначе только первое видео)"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Подавить вывод прогресса"
    )
    
    args = parser.parse_args()
    
    download_audio(
        url=args.url,
        output_dir=args.output_dir,
        format=args.format,
        playlist=args.playlist,
        quiet=args.quiet
    )


if __name__ == "__main__":
    main()