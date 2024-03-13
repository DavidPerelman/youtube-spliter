import re
import os
import eyed3
from moviepy.editor import VideoFileClip
from extract_chapters_from_description import split_line

def export_data(lines, start_times, titles, end_times, video_length):
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
        
                # Iterate over the start_times list
        for i in range(len(start_times)):
            # If it's not the last element, set the end time to the next value in start_times
            if i < len(start_times) - 1:
                if len(start_times[i + 1]) == 5:
                    start_times[i + 1] = f"00:{start_times[i + 1]}"
                if len(start_times[i + 1]) == 7:
                    start_times[i + 1] = f"0{start_times[i + 1]}"
                end_times.append(start_times[i + 1])
            else:
                # For the last element, set the end time to None or any other appropriate value
                end_times.append(None)

        if start_times:
            start_times[0] = "00:00:00"

        if end_times:
            end_times[-1] = video_length
            
        # # Create chapters_data
        chapters_data = {
            'start': start_times,
            'end': end_times,
            'title': titles,
        }

        return chapters_data

def split_line_to_data(line, video_length):
    # Initialize lists to store times and titles
    start_times = []
    titles = []
    end_times = []

    # Split line into start time and title
    parts = line.split(' ')
    start_time = parts[0].strip()
    str = " "
    title = str.join(parts[1:]).title()
    
    if len(start_time) == 5:
        start_time = f"00:{start_time}"
    if len(start_time) == 7:
        start_time = f"0{start_time}"

    # # Append start time and title to lists
    start_times.append(start_time)
    titles.append(title)

    return {'start_time': start_time, 'title': title}

def add_tags(input_dir, album_name, artist_name, recording_date):
    try:
        for file_name in os.listdir(input_dir):
            if file_name.endswith(".mp3"):
                audio_file_path = os.path.join(input_dir, file_name)
                audio_file = eyed3.load(audio_file_path)

                audio_file.tag.artist = artist_name
                audio_file.tag.title = file_name[3:-4]
                audio_file.tag.album = album_name
                audio_file.tag.recording_date = recording_date
                audio_file.tag.track_num = file_name[:2]
                audio_file.tag.save()
    except Exception as e:
        print(f"Error: {e}")

def get_video_length(filename):
    # Load the video clip
    clip = VideoFileClip(filename)
    
    # Get the duration of the video in seconds
    duration_seconds = clip.duration
    
    # Convert duration to hh:mm:ss format
    hours = int(duration_seconds // 3600)
    minutes = int((duration_seconds % 3600) // 60)
    seconds = int(duration_seconds % 60)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def read_text(text_path):
    file = open(text_path, "r")
    content = file.read()
    file.close()
    return content

def create_chapters_data(text_content, video_length, type):
    # Initialize lists to store times and titles
    start_times = []
    titles = []
    end_times = []
    # Split text into lines
    lines = text_content.strip().split('\n')

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

        chapters_data = export_data(lines, start_times, titles, end_times, video_length)
        return chapters_data
    
    if type == 'description':
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

        chapters_data = export_data(lines, start_times, titles, end_times, video_length)
        return chapters_data

def split_audio_files(artist_name, album_name, recording_date, chapters_data, video_path):
    try:
        # Create the output folder if it doesn't exist
        folder_name = r'download\{}- {} ({})'.format(artist_name, album_name, recording_date)
        os.makedirs(folder_name, exist_ok=True)

        # Loop through the lists and create subclips
        for idx, (start, end, title) in enumerate(zip(chapters_data['start'], chapters_data['end'], chapters_data['title']), start=1):
            # Convert start and end times to seconds
            start_seconds = sum(x * int(t) for x, t in zip([3600, 60, 1], start.split(':')))
            end_seconds = sum(x * int(t) for x, t in zip([3600, 60, 1], end.split(':')))
            
            # Get subclip
            sub_clip = VideoFileClip(video_path).subclip(start_seconds, end_seconds)

            # Extract audio
            audio_clip = sub_clip.audio

            # Write subclip with title as filename
            audio_clip.write_audiofile(os.path.join(folder_name, f'{idx:02d} {title}.mp3'))

            add_tags(folder_name, album_name, artist_name, recording_date)

    except OSError:
        # Ignore OSError
        pass

def create_audio(video_path):
    # Create the output folder if it doesn't exist
    os.makedirs('download', exist_ok=True)

    # Get subclip
    sub_clip = VideoFileClip(video_path)

    # Extract audio
    audio_clip = sub_clip.audio

    title = os.path.basename(video_path[:-4])

    # Write subclip with title as filename
    audio_clip.write_audiofile(os.path.join('download', f'{title}.mp3'))