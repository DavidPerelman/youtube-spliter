import os
import re
import tkinter
from tkinter import filedialog
import customtkinter

from main import start_run
from utils import create_chapters_data
from yt_api import get_fake_video_comments, get_fake_video_length, get_video_data
from yt_api_utils import extract_video_duration, extract_video_timestamps_from_comments, extract_video_timestamps_from_description

def disable_upload_file():
    upload_file_button.configure(state=tkinter.DISABLED)

def upload_file():
    global filename
    f_types = [('Text Files', '*.txt')]
    filename = filedialog.askopenfilename(
        initialdir=f'{os.getcwd()}\chapters_files',
        title="Select Text File",
        filetypes=f_types
    )

def checkbox_event():
    if check_timestamps_in_file_var.get() == False:
        upload_file_button.configure(state=tkinter.DISABLED)
    else:
        upload_file_button.configure(state=tkinter.NORMAL)
        
    if check_timestamps_in_desc_var.get():
        timestamps_in_comments.configure(state=tkinter.DISABLED)
        timestamps_in_file.configure(state=tkinter.DISABLED)
        # upload_file_button.configure(state=tkinter.DISABLED)
    else:
        timestamps_in_comments.configure(state=tkinter.NORMAL)
        timestamps_in_file.configure(state=tkinter.NORMAL)
        # upload_file_button.configure(state=tkinter.DISABLED)

        if check_timestamps_in_comments_var.get():
            timestamps_in_desc.configure(state=tkinter.DISABLED)
            timestamps_in_file.configure(state=tkinter.DISABLED)
            # upload_file_button.configure(state=tkinter.DISABLED)
        else:
            timestamps_in_desc.configure(state=tkinter.NORMAL)
            timestamps_in_file.configure(state=tkinter.NORMAL)
            # upload_file_button.configure(state=tkinter.DISABLED)

            if check_timestamps_in_file_var.get():
                timestamps_in_desc.configure(state=tkinter.DISABLED)
                timestamps_in_comments.configure(state=tkinter.DISABLED)
                # upload_file_button.configure(state=tkinter.NORMAL)
            else:
                timestamps_in_desc.configure(state=tkinter.NORMAL)
                timestamps_in_comments.configure(state=tkinter.NORMAL)
                # upload_file_button.configure(state=tkinter.NORMAL)

        
def submit():
    # print(filename)
    # print(video_url.get())
    video_id = ''
    video_url = 'https://www.youtube.com/watch?v=36GNdaxlA0k'

    print(video_url)
    
    # Regular expression pattern to match YouTube video IDs
    pattern = r"(?<=v=)[a-zA-Z0-9_-]+(?=&|$)"

    # Search for the video ID in the URL
    match = re.search(pattern, video_url)

    # If a match is found, set the video ID
    if match:
        video_id = match.group(0)
    
    if check_timestamps_in_desc_var.get() == True:
        # Extract data from response:
        # video_response = get_fake_video_length()
        video_response = get_video_data(video_id, 'description')

        # Extract duration from video data:
        video_length = extract_video_duration(video_response)

        # Extract timestamps from video response:
        description = video_response['items'][0]['snippet']['description']
        # description = description_response['items'][0]['snippet']['description']
        description_video_timestamps = create_chapters_data(description, video_length, 'text_file')
        start_run(video_url, description_video_timestamps, 'Live At Southside Music Festival', 'Twenty One Pilots', 2022)
        # start_run(video_id, description_video_timestamps, album_name.get(), artist_name.get(), recording_date.get())
    elif check_timestamps_in_comments_var.get() == True:
        # Extract data from response:
        # comments_response = get_fake_video_comments()
        comments_response = get_video_data(video_id, 'comments')
        duration_response = get_video_data(video_id, 'description')

        # Extract duration from video data:
        video_length = extract_video_duration(duration_response)

        # Extract timestamps from response:
        comments_video_timestamps = extract_video_timestamps_from_comments(comments_response, video_length)
        
        # start_run(video_id, comments_video_timestamps, album_name.get(), artist_name.get(), recording_date.get())
        start_run(video_url, comments_video_timestamps[0], 'Live At Glastonbury', 'Arctic Monkeys', 2007)
    elif check_timestamps_in_file_var.get() == True:
        # # Extract duration from text file:
        video_response = get_fake_video_length()
        video_length = extract_video_duration(video_response)

        # Extract timestamps from text file:
        file_content = open(f"{filename}", "r").read()
        description_video_timestamps = create_chapters_data(file_content, video_length, 'text_file')
        start_run(video_id, description_video_timestamps, album_name.get(), artist_name.get(), recording_date.get())
    # else:
    #     return

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

# Create a frame to hold the widgets
frame = customtkinter.CTkFrame(app, width=350, height=40, fg_color=app._fg_color)
frame.pack(padx=0, pady=15)

# Timestamps in description check box
check_timestamps_in_desc_var = customtkinter.BooleanVar(value=False)
timestamps_in_desc = customtkinter.CTkCheckBox(frame, text='There is timestamps in video description?', command=checkbox_event,
                                              variable=check_timestamps_in_desc_var, onvalue="on", offvalue="off")
timestamps_in_desc.grid(row=0, column=0, padx=(1, 0), pady=10)

# Timestamps in comments check box
check_timestamps_in_comments_var = customtkinter.BooleanVar(value=False)
timestamps_in_comments = customtkinter.CTkCheckBox(frame, text='There is timestamps in video comments?', command=checkbox_event, 
                                              variable=check_timestamps_in_comments_var, onvalue="on", offvalue="off")
timestamps_in_comments.grid(row=1, column=0, pady=10)

# # Timestamps in file check box
check_timestamps_in_file_var = customtkinter.BooleanVar(value=False)
timestamps_in_file = customtkinter.CTkCheckBox(frame, text='There is timestamps in file?', command=checkbox_event, 
                                              variable=check_timestamps_in_file_var, onvalue="on", offvalue="off")
timestamps_in_file.grid(row=2, column=0, padx=(0, 80), pady=10)

# Upload button
upload_file_button = customtkinter.CTkButton(frame, text='Upload', command=upload_file, width=40, height=30)
# button.pack(padx=1, pady=1)
upload_file_button.grid(row=2, column=1, padx=(0, 30))

# Download button
button = customtkinter.CTkButton(app, text='Download', command=submit, width=350, height=40)
button.pack(padx=20, pady=20)

disable_upload_file()

# Run app
app.mainloop()