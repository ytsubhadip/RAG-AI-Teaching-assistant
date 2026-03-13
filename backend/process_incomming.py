
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from middleware.embadding_json import create_embadding
import numpy as np
import pandas as pd
import requests
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

df = joblib.load("embaddings.joblib")
client = genai.Client(api_key=os.getenv("api_key"))

#llm model api request function
def infarence(prompt):
 
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })
    responce = r.json()
    return responce

# def infarence(prompt):
#     response = client.models.generate_content(
#         model="gemini-3-flash-preview",
#         contents=prompt
#     )
#     return (response.text)




def get_output(chat:str) :
 
    # create embedding for the question text; API returns a list of embeddings
    question_embadding = create_embadding([chat])
    # ensure we have a single vector rather than a nested list
    if isinstance(question_embadding, list) and len(question_embadding) == 1:
        question_embadding = question_embadding[0]

    # applying cosine similarity methods
    # X is (n_chunks, dim) and Y should be (1, dim)
    similarity = cosine_similarity(
        np.vstack(df["embedding"].values),
        np.array([question_embadding])
    ).flatten()
    top_results = 3
    max_index = similarity.argsort()[::-1][0:top_results]
    new_df = df.loc[max_index]

    prompt = f""" I am teaching python for biganears to advance course. Here are video subtitle chunk containing video title, video number,  start time in secound, end time secound, the text at that time:

    {new_df[["title","number","start","end","text"]].to_json(orient="records")}
    -------------------------------------------------
    '{chat}'
    User asked this question related to the video chunks, you have answare in a human way(don't mantion the above formate, its for you)where and how much content is tought in which video(in which video and what was the timestap ) and guid the user to go to that particular video. If user ask unrelated question, tell him that you can only answer question related to the course. Don't ask any question to the user. just give the question answare.
    """

    llm_responce = infarence(prompt)["response"]
    print(llm_responce)
    return llm_responce





