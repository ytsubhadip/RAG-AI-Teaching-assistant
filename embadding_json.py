import requests
import os
import json
import pandas as pd
import ollama 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib


def create_embadding(text_list):
    r = requests.post("http://localhost:11434/api/embed", json={

        "model":"bge-m3",
        "input":text_list
    }) 
    embedding = r.json()["embeddings"]
    return embedding



if __name__ == '__main__':
    jsons = os.listdir("jsons")
    chanks_id = 0
    my_dicts = []

    for json_file in jsons:
        # read json file
        with open(f"jsons/{json_file}" , encoding="utf-8") as f:
            content = json.load(f)

        print(f"creating embeding for {json_file}")
        
        #fit all chank text list to the embading function
        embaddings = create_embadding([c["text"] for c in content["chunks"]])


        for i,chuck in enumerate(content["chunks"]):
            chuck["chunk_id"] = chanks_id
            chuck["embedding"] = embaddings[i]
            my_dicts.append(chuck)
            chanks_id +=1
                  
    df = pd.DataFrame.from_records(my_dicts)
    joblib.dump(df, "embaddings.joblib")





