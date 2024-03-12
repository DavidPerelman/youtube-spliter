import os
from download_video import startDownload
from utils import create_audio, create_captures_data, get_video_length, read_text, split_audio_files

software_path = os.getcwd()

# YouTube video URL
# David Gilmour in Concert Meltdown 2001/2002
# video_url = 'https://www.youtube.com/watch?v=5hrd5Ek54VA'

# לילה כיום יאיר
video_url = 'https://www.youtube.com/watch?v=cXIbcvaWIKg'

try:
    print("\nDownloading...")

    # Download video
    video_path = startDownload(video_url)

    text_dir = os.listdir('./text_files') 

    # Checking if the text directory is empty or not 
    if len(text_dir) == 0: 
        create_audio(video_path) 
    else: 
        captures_file_name = r'{}\text_files\{}'.format(os.getcwd(), text_dir[0])

        file_size = os.stat(captures_file_name).st_size

        if file_size > 0:
            text_path = r'{}\text_files\captures.txt'.format(software_path)

            text = read_text(text_path)
            
            text_content = r"""" {} """.format(text)

            video_length = get_video_length(video_path)

            captures_data = create_captures_data(text_content, video_length)

            done = split_audio_files(captures_data, video_path)
except OSError:
    # Ignore OSError
    pass