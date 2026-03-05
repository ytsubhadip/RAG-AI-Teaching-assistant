# How to use this RAG AI Python Teaching assistant on your own data 
## Step 1 - Collect videos
Move all your video files to the videos folder

## step 2 - Convert to mp3 using FFmpeg
Convert all the video files to mp3 by running video_to_mp3

## step 3 - Convert mp3 to json using Wishper model
Convert all the mp3 files to json by running mp3_to_json

## step 4 - Convert the json files to Vectors using ollama bge-m3 model
Use the file preprocess_json to convert the json files to a dataframe with Embedding and save it as a joblib file

## step 5 - Prompt generation and feeding to LLM use ollama llama3.2
Read the joblib file and load it into the memory. Then create a relevent prompt as per the user query and feed it to the LLM 
