import sqlite3

def save_ticket(query, response, confidence):

    conn = sqlite3.connect("support.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_query TEXT,
        ai_response TEXT,
        confidence REAL
    )
    """)

    cursor.execute(
        "INSERT INTO tickets (user_query, ai_response, confidence) VALUES (?, ?, ?)",
        (query, response, confidence)
    )

    conn.commit()
    conn.close()