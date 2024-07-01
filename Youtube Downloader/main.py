import tkinter
import customtkinter
from pytube import YouTube

# Download 
def startDownload():
    try:
        ytLink = link.get()
        if not ytLink.strip():
            finishLabel.configure(text="Please enter a valid YouTube link", text_color="red")
            return
        
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        # Select the highest resolution progressive stream available (includes both video and audio)
        video = ytObject.streams.filter(progressive=True).order_by('resolution').desc().first()
        
        if not video:
            finishLabel.configure(text="No suitable video stream found", text_color="red")
            return
        
        title.configure(text=ytObject.title, text_color="white")
        finishLabel.configure(text="")
        video.download()
        finishLabel.configure(text="Download Complete!", text_color="green")
        link.delete(0, tkinter.END)

    except Exception as e:
        finishLabel.configure(text="Download Error: " + str(e), text_color="red")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    pPercentage.configure(text=per + '%')
    pPercentage.update()

    progressBar.set(float(percentage_of_completion) / 100)

# Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("YouTube Downloader")

# Adding UI Elements
title = customtkinter.CTkLabel(app, text="Insert a YouTube link")
title.pack(padx=10, pady=10)

# Link input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack(pady=10)

# Progress Bar
progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(pady=10)

# Progress Percentage
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

# Finished Downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack(pady=10)

# Download button
download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(padx=10, pady=10)

# Run 
app.mainloop()
