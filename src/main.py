from ast import Break
from re import L
import tkinter as tk
import pytube
from tkinter import messagebox, filedialog
import ffmpeg
import progressbar as progress
from pytube.cli import on_progress
import os
import subprocess
import threading

class CmdThread (threading.Thread):
   def __init__(self, command, textvar):
        threading.Thread.__init__(self)
        self.command = command
        self.textvar = textvar

   def run(self):
        proc = subprocess.Popen(self.command, stdout=subprocess.PIPE)
        while not proc.poll():
            data = proc.stdout.readline()
            if data:
                print(data)
                self.textvar.set(data)
            else:
                break

def progress(streams, chunk: bytes, bytes_remaining: int):
    contentsize = video.filesize
    size = contentsize - bytes_remaining

    print('\r' + '[Download progress]:[%s%s]%.2f%%;' % (
    '█' * int(size*20/contentsize), ' '*(20-int(size*20/contentsize)), float(size/contentsize*100)), end='')
   
YT = ''
video = ''

def download():
    global video


    RES = clicked.get()

    if not url.get():
        messagebox.showinfo("Error",
                            "Enter a download link")
        return

    download_Folder = dest.get()

    if RES == "audio":
        video = YT.streams.filter(abr="160kbps", progressive=False).first()
        video.download(download_Folder, filename=f"{YT.title}.mp3")
        messagebox.showinfo("SUCCESSFULLY",
                            "DOWNLOADED AND SAVED IN\n"
                            + download_Folder)
        
    elif RES not in ['1080p', '1440p']:
        video = YT.streams.filter(res=RES, progressive=True).first()
 
        video.download(download_Folder)
    
        messagebox.showinfo("SUCCESSFULLY",
                            "DOWNLOADED AND SAVED IN\n"
                            + download_Folder)
    else:
        if download_Folder:
            download_Folder += '/'

        title = YT.title
        title = ''.join(letter for letter in title if letter.isalnum())

        # download audio only
        video = YT.streams.filter(abr="160kbps", progressive=False).first()
        video.download(download_Folder, filename="audio.mp3")
        print("\nAudio download success")

        video = YT.streams.filter(res="1080p", progressive=False).first()
        video.download(download_Folder, filename="video.mp4")
        print("\nVideo download success")

        language = ''
        for caption in YT.caption_tracks:
            if caption.name in ['English - en', 'en', 'English', 'english']:
                language = caption.name
                en_caption = caption
        # print(en_caption.xml_captions)

        if language: 
        # Instead of Captions in XML format we are converting it to string format.
            en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            with open(download_Folder+'subs.srt', "w", encoding="utf-8") as f:
                f.write(en_caption_convert_to_srt)

        try:
            #f'ffmpeg -i {download_Folder}video.mp4 -i {download_Folder}audio.mp3 -c:v copy -c:a copy {download_Folder+title}.mp4'
            if language:
                subprocess.run(['ffmpeg', '-i', download_Folder+'video.mp4', '-i',  download_Folder+"audio.mp3",'-i', download_Folder+'subs.srt' ,"-c:v", "copy", "-c:a", "copy", '-c:s', 'mov_text', download_Folder+title+'.mp4'], check=True)
            else:
                subprocess.run(['ffmpeg', '-i', download_Folder+'video.mp4', '-i', download_Folder + "audio.mp3", "-c:v", "copy", "-c:a", "copy", download_Folder+title+'.mp4'], check=True)
        except:
            # print ('wrongcommand does not exist')
            audio = ffmpeg.input(f"{download_Folder}audio.mp3")

            #download video only

            video = ffmpeg.input(f"{download_Folder}video.mp4")

            

            ffmpeg.output(audio, video, f"{download_Folder}{title}.mp4", vcodec='copy', acodec='copy').run(overwrite_output=True)

        os.remove(f"{download_Folder}audio.mp3")
        os.remove(f"{download_Folder}video.mp4")
        if language:
            os.remove(f"{download_Folder}subs.srt")
        messagebox.showinfo("SUCCESSFULLY",
                            "DOWNLOADED AND SAVED IN\n"
                            + download_Folder)


def videodetails():
    link = url.get()
    if not link:
        messagebox.showinfo("Error",
                            "Enter a link")
        return
    try:
        yt = pytube.YouTube(link, on_progress_callback=progress)
    except:
        messagebox.showinfo("Error",
                            "Enter a valid link")
        return


    title.config(text = f"Title: {yt.title}")
    author.config(text = f"Author: {yt.author}")
    publishDate.config(text = f"Published date: {yt.publish_date.strftime('%Y-%m-%d')}")
    views.config(text = f"Number of views: {yt.views}")
    duration.config(text=f"Length of video: {yt.length} seconds")

    resolutions = set()
    for e in yt.streams:
        for quality in ['144p',"240p", "360p", "480p", "720p", "1080p", "1440p", "audio"]:
            if quality in str(e):
                resolutions.add(quality)


    resolutions = sorted(list(resolutions), key= lambda x:(len(x), x))

    clicked.set('')
    qualitySelect['menu'].delete(0, 'end')

    # Insert list of new options (tk._setit hooks them up to var)
    for choice in resolutions:
        qualitySelect['menu'].add_command(label=choice, command=tk._setit(clicked, choice))
    clicked.set(resolutions[0])

    global YT
    YT = yt
    




def browse():
    #getting directory
    download_Directory = filedialog.askdirectory(
        initialdir="YOUR DIRECTORY PATH", title="Save Video")
 
    #inserting dir in the textbox
    dest.insert(0, download_Directory) 


#MAIN
root = tk.Tk()
# root.iconbitmap('info.ico')
root.geometry("")
root.resizable(False, False)
root.title("Youtube Downloader")
root.eval('tk::PlaceWindow . center')
#root.config(background="#e87878")

root.option_add( "*font", "lucida 10" )

#labels
label1 = tk.Label(root, 
                text = "Youtube link: ",
                padx=10,
                pady=10)

label2 = tk.Label(root, 
                text="Destination: ", 
                padx=10,
                pady=5)

title = tk.Label(root, text="Title:",padx=10,
                pady=10)
author = tk.Label(root, text="Author:",padx=10,
                pady=10)
publishDate = tk.Label(root, text="Published date:",padx=10,
                pady=10)
views = tk.Label(root, text="Number of views:",padx=10,
                pady=10)
duration = tk.Label(root, text="Length of video:",padx=10,
                pady=10)


text = tk.StringVar()
downloadProgress = tk.Label(textvariable=text)

thread = CmdThread(['ipconfig'], text)

#buttons
browse = tk.Button(root,
                text="Browse",
                command=browse,
                width=10)

download = tk.Button(root, 
                        text = "Download", 
                        command = download, bg='#567', fg='White')

getDetails = tk.Button(root, text = "Get Details", command=videodetails)


clicked = tk.StringVar()
qualitySelect = tk.OptionMenu(root, clicked,'')
# qualitySelect.pack()

#inputs
url = tk.Entry(root, width=35)
dest = tk.Entry(root)

#ui

label1.grid(row=2,
                column=0,
                pady=5,
                padx=5)

url.grid(row=2,
            column=1,
            pady=5,
            padx=5,
            columnspan=2)

getDetails.grid(row=2, column=3,
                pady=20,
                padx=20)

label2.grid(row=3,
            column=0,
            pady=5,
            padx=5)

dest.grid(row=3,
            column=1,
            pady=5,
            padx=5)

browse.grid(row=3,
            column=2,
                pady=1,
                padx=1)

qualitySelect.grid(row=4,
                column=3)

download.grid(row=5,
                column=3)

title.grid(row=4,column=1)
author.grid(row=5,column=1)
publishDate.grid(row=6,column=1)
views.grid(row=7,column=1)
duration.grid(row=8,column=1)
# downloadProgress.grid(row=9, column=1, pady=5)
messagebox.showinfo("INFO",
                        "Console will show the download progress and Errors.\n \nDownloading videos higher than 720p requires ffmpeg installed on you computer and download time will depend on computer hardware.")

# qualitySelect.grid(row=)

# thread.start()

root.mainloop()
