from .db import get_db_connection

def handle_feedback(form, session):
    feedback_text = form.get("feedback_text", "").strip()
    category = form.get("category", "general")
    email = form.get("email", "").strip()

    if not feedback_text:
        return False, "Feedback cannot be empty."

    user_id = None
    if 'username' in session:
        # get the user_id
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE LOWER(username) = LOWER(%s)", (session['username'],))
            row = cursor.fetchone()
        conn.close()
        if row:
            user_id = row[0]

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO feedback (user_id, email, category, feedback_text)
            VALUES (%s, %s, %s, %s)
        """, (user_id, email, category, feedback_text))
        conn.commit()
    conn.close()

    return True, "Thanks for your feedback!"