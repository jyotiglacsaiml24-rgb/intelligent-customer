from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from ai_service import generate_response
from database import save_ticket
import sqlite3

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Query(BaseModel):
    message: str
@app.post("/chat")
def chat(query: Query):
    response, confidence = generate_response(query.message)
    save_ticket(query.message, response, confidence)

    if confidence < 0.7:
        return {
            "response": "I am not confident. Escalating to human agent.",
            "confidence": confidence,
            "escalate": True
        }

    return {
        "response": response,
        "confidence": confidence,
        "escalate": False
    }



@app.get("/tickets")
def get_tickets():

    conn = sqlite3.connect("support.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets")
    data = cursor.fetchall()

    conn.close()

    return {"tickets": data}



@app.post("/feedback")
def feedback(data: dict):

    query = data.get("query")
    response = data.get("response")

    conn = sqlite3.connect("support.db")
    cursor = conn.cursor()

    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_query TEXT,
        agent_response TEXT
    )
    """)

    
    cursor.execute(
        "INSERT INTO feedback (user_query, agent_response) VALUES (?, ?)",
        (query, response)
    )

    conn.commit()
    conn.close()

    return {"message": "Feedback saved successfully"}
