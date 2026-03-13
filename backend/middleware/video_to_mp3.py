import os
import subprocess

files = os.listdir("video")
for file in files:
    tutorial_number = (file.split('-')[0])
    file_name = file.split('｜')[0].split('-',1)[1].strip()

    subprocess.run(["ffmpeg","-i",f"video/{file}",f"audios/{file_name}_{tutorial_number}.mp3"])
    
    
    
