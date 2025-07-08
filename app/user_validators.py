"""
Validation utilities for user registration.

Provides functions to check if a username or email is already taken in the database.
"""
from .db import get_db_connection; ## get the database connection to check for the username and emails already in the db

def is_username_available(username):
    """
    Checks whether a given username is available (not already used).

    Args:
        username (str): The username to check.

    Returns:
        tuple: (bool, str) indicating availability status and a message.
    """
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
    """
    Checks whether a given email address is available (not already registered).

    Args:
        email (str): The email address to check.

    Returns:
        tuple: (bool, str) indicating availability status and a message.
    """
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
