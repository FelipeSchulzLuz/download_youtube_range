import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
import os

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")

        self.link_label = tk.Label(root, text="YouTube Link")
        self.link_label.pack()
        self.link_entry = tk.Entry(root, width=50)
        self.link_entry.pack()

        self.range_frame = tk.Frame(root)
        self.range_frame.pack()
        self.start_label = tk.Label(self.range_frame, text="Start (min:sec)")
        self.start_label.grid(row=0, column=0)
        self.start_entry = tk.Entry(self.range_frame, width=10)
        self.start_entry.grid(row=0, column=1)

        self.end_label = tk.Label(self.range_frame, text="End (min:sec)")
        self.end_label.grid(row=1, column=0)
        self.end_entry = tk.Entry(self.range_frame, width=10)
        self.end_entry.grid(row=1, column=1)

        self.download_audio_button = tk.Button(root, text="Download Audio", command=self.download_audio)
        self.download_audio_button.pack()

        self.download_video_button = tk.Button(root, text="Download Video Segment", command=self.download_video_segment)
        self.download_video_button.pack()

    def download_audio(self):
        link = self.link_entry.get()
        start_time = self.start_entry.get()
        end_time = self.end_entry.get()
        
        if not link:
            messagebox.showerror("Error", "Please enter a YouTube link.")
            return
        if not start_time or not end_time:
            messagebox.showerror("Error", "Please enter both start and end times.")
            return

        yt = YouTube(link)
        audio_stream = yt.streams.filter(only_audio=True).first()
        download_path = filedialog.askdirectory()

        if not download_path:
            return

        audio_file = audio_stream.download(output_path=download_path)
        base, ext = os.path.splitext(audio_file)
        new_file = base + '.mp3'
        os.rename(audio_file, new_file)

        start_min, start_sec = map(int, start_time.split(':'))
        end_min, end_sec = map(int, end_time.split(':'))
        start = start_min * 60 + start_sec
        end = end_min * 60 + end_sec

        audio_clip = AudioFileClip(new_file).subclip(start, end)
        output_file = os.path.join(download_path, f"{yt.title}_segment_audio.mp3")
        audio_clip.write_audiofile(output_file)

        messagebox.showinfo("Success", f"Audio segment downloaded: {output_file}")

    def download_video_segment(self):
        link = self.link_entry.get()
        start_time = self.start_entry.get()
        end_time = self.end_entry.get()
        
        if not link:
            messagebox.showerror("Error", "Please enter a YouTube link.")
            return
        if not start_time or not end_time:
            messagebox.showerror("Error", "Please enter both start and end times.")
            return

        yt = YouTube(link)
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        download_path = filedialog.askdirectory()

        if not download_path:
            return

        video_file = video_stream.download(output_path=download_path)

        start_min, start_sec = map(int, start_time.split(':'))
        end_min, end_sec = map(int, end_time.split(':'))
        start = start_min * 60 + start_sec
        end = end_min * 60 + end_sec

        video_clip = VideoFileClip(video_file).subclip(start, end)
        output_file = os.path.join(download_path, f"{yt.title}_segment.mp4")
        video_clip.write_videofile(output_file, codec="libx264")

        messagebox.showinfo("Success", f"Video segment downloaded: {output_file}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()