import sqlite3

def generate_response(message):

    message = message.lower()

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
        "SELECT agent_response FROM feedback WHERE user_query=?",
        (message,)
    )

    result = cursor.fetchone()

    if result:
        conn.close()
        return result[0], 0.95   

    conn.close()

    if "refund" in message:
        return "Refund takes 5-7 business days.", 0.9

    elif "return" in message:
        return "You can return products within 7 days.", 0.9

    elif "order" in message:
        return "You can track your order in the orders section.", 0.9

    elif "cancel" in message:
        return "Order can be cancelled before shipping.", 0.85

    elif "payment" in message:
        return "We support UPI, Credit Card, and Debit Card.", 0.85

    return "I am not confident. Escalating to human agent.", 0.5
