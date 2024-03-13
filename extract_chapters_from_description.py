import re
from pytube import YouTube

def get_desc(url):
    youtube = YouTube(url)
    stream = youtube.streams.first()
    desc = youtube.initial_data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['attributedDescription']['content']
    return desc

def search_description(video_url):
    # Create a YouTube object
    youtube = YouTube(video_url)

    stream = youtube.streams.first()

    print(youtube.description)
    
def extract_chapters_from_description(description):
    chapters = []
    
    # Split description into lines
    lines = description.split("\n")
    
    # Define regex pattern to match time stamps
    time_pattern = re.compile(r"\d+:\d+:\d+")
    
    for line in lines:
        # Search for time stamps in the line
        matches = re.findall(time_pattern, line)
        if matches:
            # Extract time stamp and chapter title
            timestamp = matches[0]
            title = line.replace(timestamp, "").strip()
            chapters.append({"timestamp": timestamp, "title": title})
    
    return chapters

# # Example usage
# description = """00:00:00 "Heathens"
# 00:03:26 "Morph"
# 00:05:22 "Holding on to You"
# 00:07:54 "The Outside"
# 00:13:45 "Lane Boy"
# 00:17:17 "Chlorine"
# 00:21:40 "Mulberry Street"
# 00:27:01 "Campfire Set"
# 00:37:26 "Jumpsuit"
# 00:41:12 "Heavydirtysoul"
# 00:44:50 "Saturday"
# 00:50:16 "Level of Concern"
# 00:52:17 "Ride"
# 00:56:22 "Car Radio"
# 1:01:52 "Stressed Out"
# 1:09:08 "Shy Away"
# 1:14:13 "Trees"
# """

# chapters = extract_chapters_from_description(description)
# for chapter in chapters:
#     print(chapter)
