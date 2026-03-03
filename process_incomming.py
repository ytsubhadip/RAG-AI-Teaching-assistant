
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from embadding_json import create_embadding
import numpy as np
import pandas as pd
import requests

df = joblib.load("embaddings.joblib")

#llm model api request function
def infarence(prompt):
 
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })
    responce = r.json()
    return responce

incoming_query = input("Enter you query: ")
question_embadding = create_embadding(incoming_query)[0]

#applying cosine similarity methods
similarity = cosine_similarity(np.vstack(df["embedding"].values), np.array([question_embadding])).flatten()
top_results = 6
max_index = similarity.argsort()[::-1][0:top_results]
new_df = df.loc[max_index]

prompt = f""" I am teaching python for biganears to advance course. Here are video subtitle chunk containing video title, video number,  start time in secound, end time secound, the text at that time:

{new_df[["title","number","start","end","text"]].to_json(orient="records")}
-------------------------------------------------
'{incoming_query}'
User asked this question related to the video chunks, you have answare in a human way(don't mantion the above formate, its for you)where and how much content is tought in which video(in which video and what was the timestap ) and guid the user to go to that particular video. If user ask unrelated question, tell him that you can only answer question related to the course. Don't ask any question to the user. just give the question answare.
"""

llm_responce = infarence(prompt)["response"]
print(llm_responce)

# save the prompt in text file
with open("responce.txt", "w") as f:
    f.write(llm_responce)


# for index, item in new_df.iterrows():
#     print(index, item["title"],":",item["text"])

