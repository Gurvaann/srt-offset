import re
from datetime import datetime, timedelta

def offset_subtitle_time(subtitle, offset_ms):
    start_time, end_time = subtitle.split(' --> ')
    start = datetime.strptime(start_time, '%H:%M:%S,%f')
    end = datetime.strptime(end_time, '%H:%M:%S,%f')
    
    new_start = start + timedelta(milliseconds=offset_ms)
    new_end = end + timedelta(milliseconds=offset_ms)
    
    return f'{new_start.strftime("%H:%M:%S,%f")[:-3]} --> {new_end.strftime("%H:%M:%S,%f")[:-3]}'

def offset_srt(file_path, offset_ms):
    with open(file_path, 'r', encoding='utf-8') as file:
        subtitles = file.read()

    subtitle_blocks = re.split(r'\n\n', subtitles)
    
    for i, block in enumerate(subtitle_blocks):
        lines = block.split('\n')
        if len(lines) >= 3:
            lines[1] = offset_subtitle_time(lines[1], offset_ms)
            subtitle_blocks[i] = '\n'.join(lines)

    offset_subtitles = '\n\n'.join(subtitle_blocks)

    with open(f'offset_{offset_ms}_{file_path}', 'w', encoding='utf-8') as output_file:
        output_file.write(offset_subtitles)


srt_file_path = input("Enter the path to your SRT file: ")
offset_value = int(input("Enter the offset in milliseconds: "))

offset_srt(srt_file_path, offset_value)
