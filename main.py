import os
from download_video import startDownload
from extract_chapters_from_description import add_end_timestamp, extract_chapters_from_description, get_desc
from utils import create_audio, create_chapters_data, get_video_length, read_text, split_audio_files

software_path = os.getcwd()

# YouTube video URL
# David Gilmour in Concert Meltdown 2001/2002
# video_url = 'https://www.youtube.com/watch?v=5hrd5Ek54VA'

# לילה כיום יאיר
# video_url = 'https://www.youtube.com/watch?v=cXIbcvaWIKg'

# Twenty One Pilots - Live at Southside Music Festival (Full Set)
# video_url = 'https://www.youtube.com/watch?v=1AyWoI2e7FM'

# video_url = 'https://www.youtube.com/watch?v=lc4BL2adPeo'

try:
    video_url = input('Enter youtube link: ')
    album_name = input('Enter album name: ')
    artist_name = input('Enter artist: ')
    recording_date = input('Enter recording year: ')

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

    # # # Get video chapters from description
    chapters = extract_chapters_from_description(description)

    # # # Checking if the video chapters from description is empty or not 
    if len(chapters) > 0:
            chapters_data = add_end_timestamp(chapters, video_length)

            done = split_audio_files('artist_name', 'album_name', 2002, chapters_data, video_path)
    # # # Checking if the text directory is empty or not 
    elif len(text_dir) > 0: 
    # # # Checking if the text chapters belongs to the video 
        if f'{video_name}.txt' in text_dir:
            text_path = r'{}\chapters_files\{}.txt'.format(software_path, video_name)

            text = read_text(text_path)
                
            text_content = r""" {} """.format(text)

            chapters_data = create_chapters_data(text_content, video_length)

            done = split_audio_files(artist_name, album_name, recording_date, chapters_data, video_path)
        else: 
        # # # Create single audio file
            create_audio(video_path) 
except OSError:
    # Ignore OSError
    pass