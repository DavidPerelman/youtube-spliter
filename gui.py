import tkinter
import customtkinter

from main import start_run

def submit():
    start_run(video_url.get(), album_name.get(), artist_name.get(), recording_date.get())
    # label.configure(text=my_entry.get())

# System Setting
customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('blue')

# Our app frame
app = customtkinter.CTk()
app.geometry('720x480')
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

# Download button
button = customtkinter.CTkButton(app, text='Download', command=submit, width=350, height=40)
button.pack(padx=20, pady=20)

# Run app
app.mainloop()