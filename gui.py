import re
import tkinter
import customtkinter

from main import start_run
from yt_api import get_fake_video_comments, get_fake_video_length, get_video_length
from yt_api_utils import extract_video_duration, extract_video_timestamps_from_comments, extract_video_timestamps_from_description

def checkbox_event():
    if check_timestamps_in_desc_var.get():
        timestamps_in_comments.configure(state=tkinter.DISABLED)
        timestamps_in_file.configure(state=tkinter.DISABLED)
    else:
        timestamps_in_comments.configure(state=tkinter.NORMAL)
        timestamps_in_file.configure(state=tkinter.NORMAL)

        if check_timestamps_in_comments_var.get():
            timestamps_in_desc.configure(state=tkinter.DISABLED)
            timestamps_in_file.configure(state=tkinter.DISABLED)
        else:
            timestamps_in_desc.configure(state=tkinter.NORMAL)
            timestamps_in_file.configure(state=tkinter.NORMAL)

            if check_timestamps_in_file_var.get():
                timestamps_in_desc.configure(state=tkinter.DISABLED)
                timestamps_in_comments.configure(state=tkinter.DISABLED)
            else:
                timestamps_in_desc.configure(state=tkinter.NORMAL)
                timestamps_in_comments.configure(state=tkinter.NORMAL)

        
def submit():
    print(check_timestamps_in_desc_var.get())
    print(check_timestamps_in_comments_var.get())
    # print(video_url.get())
    video_id = ''
    video_url = 'https://www.youtube.com/watch?v=UMruSyngNaY'
    
    # Regular expression pattern to match YouTube video IDs
    pattern = r"(?<=v=)[a-zA-Z0-9_-]+(?=&|$)"

    # Search for the video ID in the URL
    match = re.search(pattern, video_url)

    # If a match is found, set the video ID
    if match:
        video_id = match.group(0)
    
    if check_timestamps_in_desc_var.get() == True:
        print('check_timestamps_in_desc_var')
        # Extract duration from response:
        video_response = get_fake_video_length()
        video_length = extract_video_duration(video_response)

        # Extract timestamps from description response:
        description_response = get_video_length(video_id)
        description = description_response['items'][0]['snippet']['description']
        description_video_timestamps = extract_video_timestamps_from_description(description, video_length)

        start_run(video_id, description_video_timestamps, album_name.get(), artist_name.get(), recording_date.get())
    elif check_timestamps_in_comments_var.get() == True:
        print('check_timestamps_in_comments_var')
        # # Extract duration from response:
        video_response = get_fake_video_length()
        video_length = extract_video_duration(video_response)

        # Extract timestamps from response:
        comments_response = get_fake_video_comments()
        comments_video_timestamps = extract_video_timestamps_from_comments(comments_response, video_length)

        start_run(video_id, comments_video_timestamps, album_name.get(), artist_name.get(), recording_date.get())
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

# Timestamps in description check box
check_timestamps_in_desc_var = customtkinter.BooleanVar(value=False)
timestamps_in_desc = customtkinter.CTkCheckBox(app, text='There is timestamps in video description?', command=checkbox_event,
                                              variable=check_timestamps_in_desc_var, onvalue="on", offvalue="off")
timestamps_in_desc.pack(padx=1, pady=20)

# Timestamps in comments check box
check_timestamps_in_comments_var = customtkinter.BooleanVar(value=False)
timestamps_in_comments = customtkinter.CTkCheckBox(app, text='There is timestamps in video comments?', command=checkbox_event, 
                                              variable=check_timestamps_in_comments_var, onvalue="on", offvalue="off")
timestamps_in_comments.pack(padx=1, pady=1)

# Timestamps in file check box
check_timestamps_in_file_var = customtkinter.BooleanVar(value=False)
timestamps_in_file = customtkinter.CTkCheckBox(app, text='There is timestamps in file?', command=checkbox_event, 
                                              variable=check_timestamps_in_file_var, onvalue="on", offvalue="off")
timestamps_in_file.pack(padx=1, pady=1)

# Download button
button = customtkinter.CTkButton(app, text='Download', command=submit, width=350, height=40)
button.pack(padx=20, pady=20)

# Run app
app.mainloop()