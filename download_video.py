import os
from pytube import YouTube

def startDownload(video_url):
    try:
        # Create the output folder if it doesn't exist
        os.makedirs('download', exist_ok=True)
        # Create a YouTube object
        yt = YouTube(video_url)

        # Get the video stream with the highest resolution
        stream = yt.streams.get_highest_resolution()

        # Download the video to the destination folder
        video_stream = stream.download(output_path='download')

        # Get the path of the downloaded audio
        return video_stream
    except:
        print('There YouTube link invalid')