import os
import shutil
from moviepy.editor import VideoFileClip

def move_directory(source_dir, destination_dir):
    try:
        # Create the output folder if it doesn't exist
        os.makedirs('download', exist_ok=True)

        # fetch all files
        for file_name in os.listdir(source_dir):
            # construct full file path
            source = source_dir + file_name
            print(source)
            destination = destination_dir + file_name
            # move only files
            if os.path.isfile(source):
                shutil.move(source, destination)
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

def create_chapters_data(text_content, video_length):
    # Split text into lines
    lines = text_content.strip().split('\n')

    # Initialize lists to store start times and titles
    start_times = []
    titles = []

    # Process each line
    for line in lines:
        # Split line into start time and title
        parts = line.split('"')
        start_time = parts[0].strip()
        title = parts[1].strip()

        # Append start time and title to lists
        start_times.append(start_time)
        titles.append(title)
        
    # Initialize the end_times list
    end_times = []

    # Iterate over the start_times list
    for i in range(len(start_times)):
        # If it's not the last element, set the end time to the next value in start_times
        if i < len(start_times) - 1:
            end_times.append(start_times[i + 1])
        else:
            # For the last element, set the end time to None or any other appropriate value
            end_times.append(None)

    if end_times:
        end_times[-1] = video_length

    # # Create chapters_data
    chapters_data = {
        'start': start_times,
        'end': end_times,
        'title': titles,
    }

    return chapters_data

def split_audio_files(video_name, chapters_data, video_path):
    try:
        # Create the output folder if it doesn't exist
        os.makedirs(r'download\{}'.format(video_name), exist_ok=True)

        os.makedirs('audio_files', exist_ok=True)

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
            audio_clip.write_audiofile(os.path.join(r'download\{}'.format(video_name), f'{idx:02d} {title}.mp3'))
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