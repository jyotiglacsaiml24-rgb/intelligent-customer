from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_db():
    conn = sqlite3.connect("support.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT,
        response TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.get("/")
def home():
    return {"message": "AI Support API Running"}


@app.post("/chat")
def chat(data: dict):
    try:
        query = data.get("query")

        if not query:
            return {"error": "Query required"}

        response = f"AI Response for: {query}"

        conn = sqlite3.connect("support.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tickets (query, response) VALUES (?, ?)",
            (query, response)
        )

        conn.commit()
        conn.close()

        return {
            "response": response,
            "confidence": 0.85
        }

    except Exception as e:
        return {"error": str(e)}

@app.get("/tickets")
def get_tickets():
    try:
        conn = sqlite3.connect("support.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tickets")
        rows = cursor.fetchall()

        conn.close()

        tickets = []
        for row in rows:
            tickets.append({
                "id": row[0],
                "query": row[1],
                "response": row[2]
            })

        return {"tickets": tickets}

    except Exception as e:
        return {"error": str(e)}
