import re
from pytube import YouTube

def get_desc(url):
    youtube = YouTube(url)
    stream = youtube.streams.first()
    desc = youtube.initial_data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['attributedDescription']['content']
    return desc

timestamp_pattern = re.compile(r"\d+:\d+")

def split_line(line):
    # Find the timestamp in the line
    match = re.search(timestamp_pattern, line)
    if(len(match.group()) == 5):
        timestamp = match.group()
        title = line.replace(timestamp, "").strip()
        return {"timestamp_start": timestamp, "title": title}
    if(len(match.group()) == 4):
        match = re.search(re.compile(r"\d+:\d+:\d+"), line)
        timestamp = match.group()
        # Remove the timestamp from the line to get the title
        title = line.replace(timestamp, "").strip()
        return {"timestamp_start": timestamp, "title": title}
    else:
        return None
    
def extract_chapters_from_description(description):
    chapters = []
    
    # Split description into lines
    lines = description.split("\n")
    
    # Define regex pattern to match time stamps
    time_pattern_1 = re.compile(r"\d+:\d+")
    time_pattern_2 = re.compile(r"\d+:\d+:\d+")
    
    for line in lines:
        # Search for time stamps in the line
        matches = re.findall(time_pattern_1, line) or re.findall(time_pattern_2, line)
        if matches:
            split_line(line)
            result = split_line(line)
            chapters.append(result)
    return chapters

def add_end_timestamp(timestamps, video_length):
    chapters = []
    # Loop through the list
    for i in range(len(timestamps) - 1):
        timestamps[i]['timestamp_end'] = timestamps[i + 1]['timestamp_start']

    # Set 'timestamp_end' of the last item to None
    timestamps[-1]['timestamp_end'] = None

    # Print the updated list
    for item in timestamps:
        chapters.append(item)

    first_item = chapters[0]
    first_item["timestamp_start"] = '00:00'

    last_item = chapters[-1]
    last_item["timestamp_end"] = video_length

    for chapter in chapters:
        if len(chapter['timestamp_start']) == 5:
            chapter['timestamp_start'] = f"00:{chapter['timestamp_start']}"
        if len(chapter['timestamp_end']) == 5:
            chapter['timestamp_end'] = f"00:{chapter['timestamp_end']}"
        if len(chapter['timestamp_start']) == 7:
            chapter['timestamp_start'] = f"0{chapter['timestamp_start']}"
        if len(chapter['timestamp_end']) == 7:
            chapter['timestamp_end'] = f"0{chapter['timestamp_end']}"

    start_times = []
    end_times = []
    titles = []
        
    for chapter in chapters:
        start_times.append(chapter['timestamp_start'])
        end_times.append(chapter['timestamp_end'])
        titles.append(chapter['title'])

    chapters_data = {
        'start': start_times,
        'end': end_times,
        'title': titles,
    }

    return chapters_data