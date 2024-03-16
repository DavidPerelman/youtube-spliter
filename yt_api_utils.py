import re

from utils import export_data, split_line_to_data

def extract_video_duration(video_response):
    # Extract duration from response
    duration = video_response['items'][0]['contentDetails']['duration']

    # Parse the duration using regular expression
    match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', duration)
    hours = int(match.group(1)[:-1]) if match.group(1) else 0
    minutes = int(match.group(2)[:-1]) if match.group(2) else 0
    seconds = int(match.group(3)[:-1]) if match.group(3) else 0

    # Calculate total length in seconds
    video_length = f"0{hours}:{minutes}:{seconds}"

    return video_length

def extract_video_timestamps_from_comments(comments, video_length):
    html_text = ''
    # Regular expression pattern to match chapter timestamps
    pattern = r'(?<!href=\")(?:\d+:)?\d+:\d+'  # Matches patterns like '0:00', '03:28', etc.

    # Loop through the comments and check for chapter timestamps
    for comment in comments:
        text = comment['textDisplay']
        
        # Use regular expression to find chapter timestamps in the comment text
        matches = re.findall(pattern, text)
        
        # If timestamps are found, print the comment and timestamps
        if matches:
            if len(text) > 100:
                html_text = text

    # Regular expression pattern to match the titles between <a> and <br> tags
    pattern = r'<a[^>]*>(.*?)<\/a>(?:<\/a>)?\s*([^<]*)(?:<br>|\s*\Z)'

    # Use regular expression to find titles in the HTML text
    titles = re.findall(pattern, html_text)

    data = [{
        "title": [],
        "start": [],
        "end": [],
    }]

    # Print the extracted titles
    for time, title in titles:
        if len(time) == 4:
                time = f"00:0{time.strip()}"
                data[0]['start'].append(time)
        if len(time) == 5:
                time = f"00:{time.strip()}"
                data[0]['start'].append(time)
        if len(time) == 7:
                time = f"0{time.strip()}"
                data[0]['start'].append(time)
        data[0]['title'].append(title.strip().title())
    
    for i in range(len(data[0]['start'])):
        if i < len(data[0]['start']) - 1:
            data[0]['end'].append(data[0]['start'][i + 1])

    data[0]['start'][0] = "00:00:00"
    data[0]['end'].append(video_length)

    print(len(data[0]['title']))
    print(len(data[0]['start']))
    print(len(data[0]['end']))

    return data

def extract_video_timestamps_from_description(description, video_length):
    # Initialize lists to store times and titles
    start_times = []
    titles = []
    end_times = []
    # Split text into lines
    lines = description.strip().split('\n')

    if type == 'text_file':
        # Define regex pattern to match time stamps
        time_pattern_1 = re.compile(r"\d+:\d+")
        time_pattern_2 = re.compile(r"\d+:\d+:\d+")
    
        for line in lines:
        # Search for time stamps in the line
            matches = re.findall(time_pattern_1, line) or re.findall(time_pattern_2, line)
            if matches:
                data = split_line_to_data(line, video_length)
                start_times.append(data['start_time'])
                titles.append(data['title'])

    chapters_data = export_data(start_times, titles, end_times, video_length)
    return chapters_data