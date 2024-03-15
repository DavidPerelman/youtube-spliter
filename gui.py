import re
import tkinter
import customtkinter

from main import start_run
from yt_api import get_fake_video_comments, get_fake_video_length
from yt_api_utils import extract_video_duration, extract_video_timestamps_from_comments

def submit():
    # print(video_url.get())
    video_id = ''
    video_url = 'https://www.youtube.com/watch?v=GtPUOFra8nE'
    
    # Regular expression pattern to match YouTube video IDs
    pattern = r"(?<=v=)[a-zA-Z0-9_-]+(?=&|$)"

    # Search for the video ID in the URL
    match = re.search(pattern, video_url)

    # If a match is found, set the video ID
    if match:
        video_id = match.group(0)
    
    if check_timestamps_in_desc_var.get() == True:
        true_label.configure(text='True')
    else:
        true_label.configure(text='False')

    if check_timestamps_in_comments_var.get() == True:
        true_label.configure(text='True')
        # # Extract duration from response:
        video_response = get_fake_video_length()
        video_length = extract_video_duration(video_response)

        # Extract timestamps from response:
        comments_response = get_fake_video_comments()
        video_timestamps = extract_video_timestamps_from_comments(comments_response, video_length)

        start_run(video_id, video_timestamps, album_name.get(), artist_name.get(), recording_date.get())
    else:
        start_run(video_id, None, album_name.get(), artist_name.get(), recording_date.get())

# System Setting
customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('blue')

# Our app frame
app = customtkinter.CTk()
app.geometry('720x620')
app.title('YouTube Splitter')

# Adding UI Elements
label = customtkinter.CTkLabel(app, text='Enter youtube link')
label.pack(padx=10, pady=10)

# Link input 
video_url = customtkinter.CTkEntry(app, width=350, height=40)
video_url.pack(padx=10)

# Adding UI Elements
label = customtkinter.CTkLabel(app, text='Enter album name')
label.pack(padx=10, pady=10)

# Album input 
album_name = customtkinter.CTkEntry(app, width=350, height=40)
album_name.pack(padx=10)

# Adding UI Elements
label = customtkinter.CTkLabel(app, text='Enter artist name')
label.pack(padx=10, pady=10)

# Album input 
artist_name = customtkinter.CTkEntry(app, width=350, height=40)
artist_name.pack(padx=10)

# Adding UI Elements
label = customtkinter.CTkLabel(app, text='Enter recording year')
label.pack(padx=10, pady=10)

# Album input 
recording_date = customtkinter.CTkEntry(app, width=350, height=40)
recording_date.pack(padx=10)

# Timestamps in description check box
check_timestamps_in_desc_var = customtkinter.BooleanVar(value=False)
timestamps_in_desc = customtkinter.CTkCheckBox(app, text='There is timestamps in video description?', 
                                              variable=check_timestamps_in_desc_var, onvalue=True, offvalue=False)
timestamps_in_desc.pack(padx=1, pady=20)

# Timestamps in comments check box
check_timestamps_in_comments_var = customtkinter.BooleanVar(value=False)
timestamps_in_comments = customtkinter.CTkCheckBox(app, text='There is timestamps in video comments?', 
                                              variable=check_timestamps_in_comments_var, onvalue=True, offvalue=False)
timestamps_in_comments.pack(padx=1, pady=1)

# Download button
button = customtkinter.CTkButton(app, text='Download', command=submit, width=350, height=40)
button.pack(padx=20, pady=20)

# Adding UI Elements
true_label = customtkinter.CTkLabel(app, text='')
true_label.pack(padx=10, pady=10)

# Run app
app.mainloop()