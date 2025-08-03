"""
feedback.py

Handles storing feedback submissions from users.
Includes optional linking to a logged-in user via session.
"""
from .db import get_db_connection

def handle_feedback(form, session):
    """
    Processes and stores user-submitted feedback in the database.

    Args:
        form (ImmutableMultiDict): The submitted feedback form containing:
            - name (str): The user's name (for anonymous feedback)
            - feedback_text (str): The user's feedback.
            - category (str): The category of feedback (default: 'general').
            - email (str): Optional email of the user.
        session (dict): Flask session containing logged-in user info.

    Returns:
        tuple: (success: bool, message: str)
            - success: True if feedback was stored, False otherwise.
            - message: Confirmation or error message.
    """
    feedback_text = form.get("feedback_text", "").strip()
    
    if not feedback_text:
        return False, "Feedback cannot be empty."
    elif len(feedback_text) > 1000:
        return False, "Feedback must be under 1000 characters."
    
    category = form.get("category", "general")
    email = form.get("email", "").strip()
    name = form.get("name", "").strip()

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
            user_id = row['id']
            name = session['username']

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO feedback (user_id, name, email, category, feedback_text)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, name, email, category, feedback_text))
        conn.commit()
    conn.close()

    return True, "Thanks for your feedback!"