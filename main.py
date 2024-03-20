import os
from download_video import startDownload
# from run_app import run_app
from utils import add_tags, create_audio, create_chapters_data, split_audio_files
from langdetect import detect

from yt_api import get_video_data
from yt_api_utils import extract_video_duration, extract_video_timestamps_from_comments

software_path = os.getcwd()

# YouTube video URL
# David Gilmour in Concert Meltdown 2001/2002
# video_url = 'https://www.youtube.com/watch?v=5hrd5Ek54VA'

# לילה כיום יאיר
# video_url = 'https://www.youtube.com/watch?v=cXIbcvaWIKg'

# Twenty One Pilots - Live at Southside Music Festival (Full Set)
# video_url = 'https://www.youtube.com/watch?v=1AyWoI2e7FM'

# Arctic Monkeys - Glastonbury 2007 Live - Full Show Remastered HD
# video_url = 'https://www.youtube.com/watch?v=36GNdaxlA0k'

def start_run(video_url, video_timestamps, album_name, artist_name, recording_date):
    try:
        album_name_lang_check = detect(album_name)
        artist_name_lang_check = detect(artist_name)

        if album_name_lang_check != 'he':
            album_name.title()

        if artist_name_lang_check != 'he':
            artist_name.title()

        print("\nDownloading...")

        # # # Download video
        video_path = startDownload(video_url)

        if len(video_timestamps) > 0:
            split_audio_files(artist_name, album_name, recording_date, video_timestamps, video_path)
            
            # Create the output folder if it doesn't exist
            folder_name = r'download\{}- {} ({})'.format(artist_name, album_name, recording_date)
            os.makedirs(folder_name, exist_ok=True)

            add_tags(folder_name, album_name, artist_name, recording_date)
        else:
            # # # Create single audio file
            create_audio(artist_name, album_name, recording_date, video_path) 
        print('Done!')
    except OSError:
        # Ignore OSError
        pass

video_url = 'https://www.youtube.com/watch?v=DWt4TlfOfjc'
album_name = 'Live (The We Meaning You Tour)'
artist_name = 'Sia'
recording_date = 2010
filepath = r"C:\Users\dpere\Documents\python-projects\youtube-spliter\chapters_files\Sia - Live (The We Meaning You Tour) (2010).txt"
type = 'timestamps_in_file'

if type == 'timestamps_in_desc':
    # Extract data from response:
    video_response = get_video_data(video_url, 'description')

    # Extract duration from video data:
    video_length = extract_video_duration(video_response)

    # Extract timestamps from video response:
    description = video_response['items'][0]['snippet']['description']
    description_video_timestamps = create_chapters_data(description, video_length, 'text_file')
    start_run(video_url, description_video_timestamps, album_name, artist_name, recording_date)
elif type == 'timestamps_in_comments':
    # Extract data from response:
    comments_response = get_video_data(video_url, 'comments')
    duration_response = get_video_data(video_url, 'description')

    # Extract duration from video data:
    video_length = extract_video_duration(duration_response)

    # Extract timestamps from response:
    comments_video_timestamps = extract_video_timestamps_from_comments(comments_response, video_length)
            
    # start_run(video_url, comments_video_timestamps, album_name, artist_name, recording_date)
elif type == 'timestamps_in_file':
    # # Extract duration from text file:
    video_response = get_video_data(video_url, 'description')
    video_length = extract_video_duration(video_response)

    # Extract timestamps from text file:
    file_content = open(f"{filepath}", "r").read()
    text_file_video_timestamps = create_chapters_data(file_content, video_length, 'text_file')
    start_run(video_url, text_file_video_timestamps, album_name, artist_name, recording_date)
# else:
    # start_run(video_url, [], 'aaa', 'aaa', 1975)