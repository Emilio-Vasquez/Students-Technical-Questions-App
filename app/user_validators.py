from .db import get_db_connection; ## get the database connection to check for the username and emails already in the db

def is_username_available(username):
    if not username:
        return False, "Username cannot be empty."
    
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE LOWER(username) = LOWER(%s)", (username,))
        existing = cursor.fetchone()
    conn.close()
    
    if existing:
        return False, "Username already taken."
    return True, "Username available."

def is_email_available(email):
    if not email:
        return False, "Email cannot be empty."
    
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE LOWER(email) = LOWER(%s)", (email,))
        existing = cursor.fetchone()
    conn.close()
    
    if existing:
        return False, "Email already in use."
    return True, "Email available."
