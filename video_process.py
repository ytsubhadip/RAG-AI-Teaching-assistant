import os
import subprocess

files = os.listdir("videos")
for file in files:
    tutorial_number = (file.split('-_')[1].split('_')[1])
    file_name = file.split("-_")[0]
    
    subprocess.run(["ffmpeg","-i",f"videos/{file}",f"audio/{file_name}{tutorial_number}.mp3"])
    print("successfull")
    
