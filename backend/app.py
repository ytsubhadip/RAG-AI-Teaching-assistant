

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from process_incomming import get_output

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all websites
    allow_credentials=True,
    allow_methods=["*"],   # allow GET, POST, etc
    allow_headers=["*"],   # allow all headers
)               

class Message(BaseModel):
    message:str

@app.get("/")
def read_root():

    return {"Devloper": "YT subhadip"}

@app.post("/getchat")
def read_item(data:Message):
    user_text = data.message
    reply = get_output(user_text)
    return {"llm responce": reply}





