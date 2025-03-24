# oka

An enhancement tool for videos that works as follows.

## Setup
Execute **make.cmd** in the dependencies folder and install the following modules.
```
pip install pillow ImageHash ffmpeg-python opencv-python --user
```

## Enhancement
Edit the **main.py** and set the arguments.
```
muse(r"C:/Users/Bob/Desktop/", 22, "normal")
muse(r"C:/Users/Bob/Desktop/", 22, "enhance")
```

## Disclaimer

:exclamation: Speeds will vary based on number of videos and file sizes.

:exclamation: The enhance video capability is around 26 minutes per video on a CPU-bound system this will vary by device.

| Capabilities | Speed |
|----|----|
| Find missing episodes | Fast |
| Find corruption | Fast |
| Convert to MP4 | Fast |
| Find duplicates | Fast |
| Enhance video | Slow |
| Remove metadata | Fast |

## Result
![](https://github.com/Apollo-o/oka/blob/1e8ea935e3151f744a98d52b105cbe31c3cbf875/video.gif)
