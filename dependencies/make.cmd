@echo off
SET path=%~dp0
SET exif="%path%exiftool_files.7z"
SET ffmpeg="%path%ffmpeg.7z"
SET root=%SystemRoot%\System32\
%root%tar.exe -xf %exif%
%root%tar.exe -xf %ffmpeg%
%root%timeout.exe /t 15 /nobreak >nul
del %exif%
del %ffmpeg%
