from ast import Break
from re import L
from tkinter import *
from pytube import YouTube
from tkinter import messagebox, filedialog


def downloadHigh():
 
    # getting user-input Youtube Link
    Youtube_link = url.get()
 
    #getting dwnld dir
    download_Folder = dest.get()
 
    # Creating object of YouTube()
    getVideo = YouTube(Youtube_link)
 
    # Getting 720p streams of the video
    videoStream = getVideo.streams.get_highest_resolution()
 
    # Downloading the video to dir
    videoStream.download(download_Folder)
 
    # popup message
    messagebox.showinfo("SUCCESSFULLY",
                        "DOWNLOADED AND SAVED IN\n"
                        + download_Folder)

def downloadLow():
 
    Youtube_link = url.get()
 
    download_Folder = dest.get()
 
    getVideo = YouTube(Youtube_link)
 
    videoStream = getVideo.streams.filter(res="360p").first()
 
    videoStream.download(download_Folder)
 
    messagebox.showinfo("SUCCESSFULLY",
                        "DOWNLOADED AND SAVED IN\n"
                        + download_Folder)


def Browse():
    #getting directory
    download_Directory = filedialog.askdirectory(
        initialdir="YOUR DIRECTORY PATH", title="Save Video")
 
    #inserting dir in the textbox
    dest.insert(0, download_Directory) 

if __name__ == "__main__":
    root = Tk()
    #root.iconbitmap('info.ico')
    root.geometry("390x200")
    root.resizable(False, False)
    root.title("Youtube Downloader")
    #root.config(background="#e87878")

    #labels
    label1 = Label(root, 
                   text = "Youtube link : ",
                   padx=10,
                   pady=10)

    label2 = Label(root, 
                   text="Destination : ", 
                   padx=10,
                   pady=5)
    
    #buttons
    browse = Button(root,
                    text="Browse",
                    command=Browse,
                    width=10)
    downloadhigh = Button(root, 
                          text = "Download 720p Quality", 
                          command = downloadHigh)
    downloadlow = Button(root, 
                         text = "Download 360p Quality", 
                         command = downloadLow)

    #inputs
    url = Entry(root, width=35)
    dest = Entry(root)

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

    downloadhigh.grid(row=4,
                  column=1,
                  pady=20,
                  padx=20)

    downloadlow.grid(row=5,
                  column=1,
                  pady=5,
                  padx=20)

    root.mainloop()