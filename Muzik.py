import os
import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp
from pathlib import Path

# Default save folder = Music folder
DEFAULT_SAVE_FOLDER = str(Path.home() / "Music")


def download_mp3():
    url = url_entry.get().strip()
    folder = folder_path.get().strip()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    if not folder:
        folder = DEFAULT_SAVE_FOLDER

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(folder, "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            },
            {
                "key": "EmbedThumbnail",
            },
            {
                "key": "FFmpegMetadata",
            }
        ],
        "writethumbnail": True,
        "quiet": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        messagebox.showinfo("Success", "MP3 downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")


def choose_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)


# ---------------- GUI ----------------

root = tk.Tk()
root.title("YouTube to MP3 Downloader")
root.geometry("500x220")
root.resizable(False, False)

# URL Label + Entry
tk.Label(root, text="YouTube Video URL:", font=("Arial", 12)).pack(pady=5)
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

# Folder selection
folder_path = tk.StringVar(value=DEFAULT_SAVE_FOLDER)

frame = tk.Frame(root)
frame.pack(pady=5)

tk.Label(frame, text="Save Location:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
folder_entry = tk.Entry(frame, textvariable=folder_path, width=40)
folder_entry.grid(row=0, column=1, padx=5)

tk.Button(frame, text="Browse", command=choose_folder).grid(row=0, column=2, padx=5)

# Download button
tk.Button(
    root,
    text="Download MP3",
    command=download_mp3,
    font=("Arial", 14),
    bg="green",
    fg="white"
).pack(pady=15)

root.mainloop()
