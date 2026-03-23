from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastApi (title="Sitat App")

def get_connection():
    return sqlite3.connect("database.db")

with get_connection() as 

class ToDo(BaseModel):
    title:str
    tasks:list

@app.post("/notat")
def nytt_notat(data:Notat):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO notes (title, text) VALUES (?, ?)"(data.title, data.text))
        conn.commit()

@app.get("/notat/{notat_id}")
