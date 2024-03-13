import re
from pytube import YouTube

def get_desc(url):
    youtube = YouTube(url)
    stream = youtube.streams.first()
    desc = youtube.initial_data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']
    if len(desc) > 0:
        if 'attributedDescription' in list(desc):
            desc = desc['attributedDescription']['content']
            return desc
        else:
            return []
        
timestamp_pattern = re.compile(r"\d+:\d+")