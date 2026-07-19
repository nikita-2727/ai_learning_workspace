import re

"""
Удаляет управляющие токены Whisper вида <|...|> из текста в функции process_audio
которые появляются в результате постобработки внутри insanely_fast_whisper_rocm
"""

file_path = '/app/insanely_fast_whisper_rocm/core/asr_backend.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Добавляем import re после from __future__ import annotations
if 'import re\n' not in content:
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('from __future__'):
            lines.insert(i + 1, 'import re')
            break
    content = '\n'.join(lines)

# 2. Находим конец импортов (первую пустую строку после импортов)
lines = content.split('\n')
insert_pos = 0
for i, line in enumerate(lines):
    if line.strip() == '' and i > 5:  # Пропускаем первые 5 строк (обычно там __future__ и комментарии)
        insert_pos = i
        break

# 3. Добавляем функцию очистки тегов ВНЕ КЛАССА
clean_func = '''
def _clean_whisper_tags(text):
    """Удаляет управляющие токены Whisper вида <|...|> из текста"""
    if isinstance(text, str):
        return re.sub(r'<\\|[^|]+\\|>', '', text).strip()
    return text
'''

if '_clean_whisper_tags' not in content:
    lines.insert(insert_pos, clean_func)
    content = '\n'.join(lines)

# 4. Добавляем очистку перед return result в функции process_audio
cleanup_code = '''
        # Очистка управляющих токенов из результата
        if 'text' in result:
            result['text'] = _clean_whisper_tags(result['text'])
        if 'chunks' in result:
            for chunk in result['chunks']:
                if 'text' in chunk:
                    chunk['text'] = _clean_whisper_tags(chunk['text'])
        if 'segments' in result:
            for segment in result['segments']:
                if 'text' in segment:
                    segment['text'] = _clean_whisper_tags(segment['text'])
'''

if '_clean_whisper_tags(result' not in content:
    lines = content.split('\n')
    in_process_audio = False
    inserted = False
    for i, line in enumerate(lines):
        if 'def process_audio' in line:
            in_process_audio = True
        if in_process_audio and 'return result' in line and not inserted:
            indent = len(line) - len(line.lstrip())
            lines.insert(i, ' ' * indent + cleanup_code.strip())
            inserted = True
            break
    content = '\n'.join(lines)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('SUCCESS: whisper tags cleanup added')