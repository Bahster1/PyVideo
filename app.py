from pytube import YouTube
import tkinter as tk
from tkinter import filedialog
import requests
import os
import concurrent.futures
from PIL import ImageTk, Image


class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=1)

        self.status = tk.StringVar()
        self.video_title = tk.StringVar()
        self.video_time = tk.StringVar()
        self.video_thumbnail = ''
        self.download_location = ''

        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label='Save Location', command=self.choose_save_directory)
        menu.add_cascade(label='File', menu=file_menu)

        self.title = tk.Label(self, text='PyVideo', bg='black', fg='white', font='none 12 bold', pady=10)

        self.status_label = tk.Label(self, textvariable=self.status, bg='black', fg='red', font='none, 10 bold',
                                     wraplength=500, pady=10)

        self.video_title_label = tk.Label(self, textvariable=self.video_title, bg='black', fg='white',
                                          font='none 10 bold', wraplength=500, pady=10)

        self.video_thumbnail_label = tk.Label(self, image=self.video_thumbnail, bg='black', height=450, width=700)

        # Save the source of image so as to not be swept away by the tkinter garbage collector
        self.video_thumbnail_label.image = self.video_thumbnail

        self.video_time_label = tk.Label(self, textvariable=self.video_time, bg='black', fg='white', font='none 8 bold',
                                         pady=5)

        self.url_input = tk.Entry(self, width=50)

        self.b1 = tk.Button(self, text='Download MP4', width=20,
                            command=lambda: concurrent.futures.ThreadPoolExecutor().submit(self.handle, 0))
        self.b2 = tk.Button(self, text='Download MP3', width=20,
                            command=lambda: concurrent.futures.ThreadPoolExecutor().submit(self.handle, 1))
        self.b3 = tk.Button(self, text='Preview', width=20,
                            command=lambda: concurrent.futures.ThreadPoolExecutor().submit(self.handle, 2))

        self.title.pack()
        self.url_input.pack()
        self.b1.pack()
        self.b2.pack()
        self.b3.pack()
        self.status_label.pack()
        self.video_title_label.pack()
        self.video_thumbnail_label.pack()
        self.video_time_label.pack()

    def handle(self, option):
        self.b1.configure(state=tk.DISABLED)
        self.b2.configure(state=tk.DISABLED)
        self.b3.configure(state=tk.DISABLED)
        self.status.set('Fetching information...')

        try:
            yt = YouTube(self.url_input.get())
            self.video_title.set(yt.title)
            self.video_thumbnail = ImageTk.PhotoImage(Image.open(
                requests.get(yt.thumbnail_url, stream=True).raw).resize((700, 450), Image.ANTIALIAS)
                                                      )
            self.video_thumbnail_label.configure(image=self.video_thumbnail)
            self.video_time.set(yt.length)

            if option == 0:
                if self.download_location == '':
                    self.choose_save_directory()
                self.status.set('Downloading video...')
                yt.streams.filter(only_video=True).first().download(os.path.abspath(self.download_location))
                self.status.set('Video has been downloaded successfully!')

            if option == 1:
                if self.download_location == '':
                    self.choose_save_directory()
                self.status.set('Downloading audio...')
                yt.streams.filter(only_audio=True).first().download(os.path.abspath(self.download_location))
                self.status.set('Audio has been downloaded successfully!')

            if option == 2:
                self.status.set('')

            self.b1.configure(state=tk.NORMAL)
            self.b2.configure(state=tk.NORMAL)
            self.b3.configure(state=tk.NORMAL)

        except Exception as e:
            self.status_label.configure(fg='red')
            self.status.set(e)

            self.b1.configure(state=tk.NORMAL)
            self.b2.configure(state=tk.NORMAL)
            self.b3.configure(state=tk.NORMAL)

    def choose_save_directory(self):
        self.download_location = os.path.abspath(filedialog.askdirectory())


def main():
    root = tk.Tk()
    app = App(root)
    app.configure(bg='black')
    root.wm_title('PyVideo')
    root.geometry('900x700')
    root.mainloop()


if __name__ == '__main__':
    main()
