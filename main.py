import os
from download_video import startDownload
from utils import add_tags, create_audio, create_chapters_data, get_video_length, read_text, split_audio_files
from pytube import YouTube

software_path = os.getcwd()

# YouTube video URL
# David Gilmour in Concert Meltdown 2001/2002
# video_url = 'https://www.youtube.com/watch?v=5hrd5Ek54VA'

# לילה כיום יאיר
# video_url = 'https://www.youtube.com/watch?v=cXIbcvaWIKg'

# Twenty One Pilots - Live at Southside Music Festival (Full Set)
# video_url = 'https://www.youtube.com/watch?v=1AyWoI2e7FM'

video_url = 'https://www.youtube.com/watch?v=lc4BL2adPeo'

try:
    album_name = input('Enter album name: ')
    artist_name = input('Enter artist: ')
    recording_date = input('Enter recording year: ')

    print("\nDownloading...")

    # Download video
    video_path = startDownload(video_url)

    video_name = os.path.basename(video_path[:-4])

    text_dir = os.listdir('./chapters_files') 

    # # Checking if the text directory is empty or not 
    if len(text_dir) == 0: 
        create_audio(video_path) 
    else: 
        text_path = r'{}\chapters_files\{}.txt'.format(software_path, video_name)

        text = read_text(text_path)
            
        text_content = r""" {} """.format(text)

        video_length = get_video_length(video_path)

        chapters_data = create_chapters_data(text_content, video_length)

        done = split_audio_files(artist_name, album_name, recording_date, chapters_data, video_path)
except OSError:
    # Ignore OSError
    pass