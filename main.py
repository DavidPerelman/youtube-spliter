import os
import pathlib
from download_video import startDownload
from utils import create_audio, create_chapters_data, get_video_length, read_text, split_audio_files, get_desc
# from langdetect import detect

software_path = os.getcwd()

# YouTube video URL
# David Gilmour in Concert Meltdown 2001/2002
# video_url = 'https://www.youtube.com/watch?v=5hrd5Ek54VA'

# לילה כיום יאיר
video_url = 'https://www.youtube.com/watch?v=cXIbcvaWIKg'

# Twenty One Pilots - Live at Southside Music Festival (Full Set)
# video_url = 'https://www.youtube.com/watch?v=1AyWoI2e7FM'

# Arctic Monkeys - Glastonbury 2007 Live - Full Show Remastered HD
# video_url = 'https://www.youtube.com/watch?v=36GNdaxlA0k'

try:
    # video_url = input('Enter youtube link: ')
    # album_name = input('Enter album name: ').title()
    # artist_name = input('Enter artist: ').title()
    # recording_date = input('Enter recording year: ')
    
    video_url = 'https://www.youtube.com/watch?v=cXIbcvaWIKg'
    album_name = 'fdfdf'.title()
    artist_name = 'fdfd'.title()
    recording_date = 2002

    # album_name_lang_check = detect(album_name)
    # artist_name_lang_check = detect(artist_name)

    # if album_name_lang_check != 'he':
    #     album_name.title()

    # if artist_name_lang_check != 'he':
    #     artist_name.title()

    print("\nDownloading...")

    # # # Download video
    video_path = startDownload(video_url)

    # # # Get video length
    video_length = get_video_length(video_path)

    # # # Get video name
    video_name = os.path.basename(video_path[:-4])

    # # # Get text folder
    text_dir = os.listdir('./chapters_files') 

    # # # Get video description
    description = get_desc(video_url)
    
    if len(description) > 0:
        # # # Get video chapters from description
        chapters = create_chapters_data(description, video_length, 'description')
        # # # Checking if the video chapters from description is empty or not 
        if len(chapters['start'] or chapters['end'] or chapters['title']) > 0:
            done = split_audio_files(artist_name, album_name, recording_date, chapters, video_path)
        # # # Checking if the text directory is empty or not 
        elif len(text_dir) > 0: 
        # # # Checking if the text chapters belongs to the video 
            if f'{video_name}.txt' in text_dir:
                text_path = r'{}\chapters_files\{}.txt'.format(software_path, video_name)

                text = read_text(text_path)
                    
                text_content = r""" {} """.format(text)

                chapters_data = create_chapters_data(text_content, video_length, 'text_file')

                done = split_audio_files(artist_name, album_name, recording_date, chapters_data, video_path)
            else: 
            # # # Create single audio file
                create_audio(artist_name, album_name, recording_date, video_path) 
    # # # Checking if the text directory is empty or not 
    elif len(text_dir) > 0: 
        # # # Checking if the text chapters belongs to the video 
        if f'{video_name}.txt' in text_dir:
            text_path = r'{}\chapters_files\{}.txt'.format(software_path, video_name)

            text = read_text(text_path)
                        
            text_content = r""" {} """.format(text)

            chapters_data = create_chapters_data(text_content, video_length, 'text_file')
            
            done = split_audio_files(artist_name, album_name, recording_date, chapters_data, video_path)
        else: 
            # # # Create single audio file
            create_audio(artist_name, album_name, recording_date, video_path) 

    print('Done!')
except OSError:
    # Ignore OSError
    pass