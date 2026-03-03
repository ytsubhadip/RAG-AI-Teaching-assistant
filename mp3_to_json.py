import whisper
import json
import os
#load whisper large-v2 model
model = whisper.load_model("large-v2")

audios = os.listdir("audio")
for audio in audios:
    number = audio.split("_")[-1].split(".")[0]
    title = audio.split("_Python")[0]
    print(f"load: {audio}")
    print("pocess..........")

    result = model.transcribe(audio=f"audio/{audio}",
                          language="hi",
                          task="translate",   
                          word_timestamps=False)
    
    chunk = []
    for segment in result["segments"]:
        chunk.append({ "number":number,
                       "title":title,
                       "start": segment["start"], 
                       "end": segment["end"],
                       "text":segment["text"] 
                        })
        
    chunks_with_metadata = {"chunks": chunk, "text":result["text"]}

    with open(f"jsons/{number}_{title}.json","w") as f:
        json.dump(chunks_with_metadata,f)
    print("successfull...")

