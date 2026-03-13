import requests
import os
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib

def create_embadding(text_list):
    # the API expects a list of inputs; wrap single strings so caller can be flexible
    if isinstance(text_list, str):
        text_list = [text_list]

    r = requests.post("http://localhost:11434/api/embed", json={
        "model":"nomic-embed-text",
        "input":text_list
    })

    embedding = r.json()["embeddings"]
    # if only one embedding was requested, return the single vector for convenience
    if isinstance(embedding, list) and len(embedding) == 1:
        return embedding[0]
    return embedding

if __name__ == '__main__':
    jsons = os.listdir("json")
    chanks_id = 0
    my_dicts = []

    for json_file in jsons:
        # read json file
        with open(f"newjsons/{json_file}" , encoding="utf-8") as f:
            content = json.load(f)

        print(f"creating embeding for {json_file}")
        
        #fit all chank text list to the embading function
        embaddings = create_embadding([c["text"] for c in content["chunks"] if c["text"].strip() != "" ])


        for i,chuck in enumerate(content["chunks"]):
            chuck["chunk_id"] = chanks_id
            chuck["embedding"] = embaddings[i]
            my_dicts.append(chuck)
            chanks_id +=1
                  
    df = pd.DataFrame.from_records(my_dicts)
    joblib.dump(df, "embaddings.joblib")





