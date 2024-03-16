import os
from download_video import startDownload
from utils import add_tags, create_audio, split_audio_files
from langdetect import detect

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