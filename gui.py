import tkinter
import customtkinter

# System Setting
customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('blue')

# Our app frame
app = customtkinter.CTk()
app.geometry('720x480')
app.title('YouTube Splitter')

# Adding UI Elements
title = customtkinter.CTkLabel(app, text='Insert a youtube link')
title.pack(padx=10, pady=10)

# Run app
app.mainloop()