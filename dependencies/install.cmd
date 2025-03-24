SET path=%~dp0
SET exif="%path%exiftool_files.7z"
SET ffmpeg="%path%ffmpeg.7z"
tar -xf %exif%
tar -xf %ffmpeg%
del %exif%
del %ffmpeg%
pip install ffmpeg-python opencv-python --user; cls