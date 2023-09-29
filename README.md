# YoutubeDownloader

Standalone exe program to download Youtube videos using their URL


Here is a new and update UI with more power compared to the previous UI

<img src="https://github.com/mohitkumar36/YoutubeDownloader/assets/57846872/de285a7c-d7ba-4e02-b478-61bdbf91e4a0" width="670" height="340">



A Python based exe program built using **pyinstaller**. 


This program is a Tkinter based GUI application which use **pytube** Python lib to help user download a Youtube video based on URL provided.


## Features
* Option to select video download quality
* Support for audio only download
* With download progress bar in the console

## Requirement(Optional)
Need [ffmpeg](https://ffmpeg.org/download.html) installed on the host PC to download video quality > 720p. \
After installing ffmpeg check if it is accessible globally by writing the below command in the PowerShell.
```
ffmpeg
```
If error pops while using the above command use alternative method to install ffmpeg.

### Alternative
I recommend using [Chocolatey](https://chocolatey.org/install) to install to avoid setting an environment variable.
![image](https://github.com/mohitkumar36/YoutubeDownloader/assets/57846872/1f86606b-54b9-4d93-9e9b-53c7962d3cf7)
After installing Chocolatey run the following command in the admin PowerShell:
```
choco install ffmpeg
```

---------------------------------------------------------------------------------------------------------------------------------------
### FOR EDUCATION PURPOSE ONLY
