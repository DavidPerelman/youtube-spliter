import re

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
        "titles": [],
        "timestamps_start": [],
        "timestamps_end": [],
    }]

    # Print the extracted titles
    for time, title in titles:
        if len(time) == 4:
                time = f"00:0{time.strip()}"
                data[0]['timestamps_start'].append(time)
        if len(time) == 5:
                time = f"00:{time.strip()}"
                data[0]['timestamps_start'].append(time)
        if len(time) == 7:
                time = f"0{time.strip()}"
                data[0]['timestamps_start'].append(time)
        data[0]['titles'].append(title.strip())
    
    for i in range(len(data[0]['timestamps_start'])):
        if i < len(data[0]['timestamps_start']) - 1:
            data[0]['timestamps_end'].append(data[0]['timestamps_start'][i + 1])

    data[0]['timestamps_start'][0] = "00:00:00"
    data[0]['timestamps_end'][-1] = video_length

    return data