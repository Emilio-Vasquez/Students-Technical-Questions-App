"""
login.py

Handles user login by validating credentials against the database.
If the credentials match, the username is stored in the session.
"""
from flask import session, flash
from .db import get_db_connection
import bcrypt

def handle_login(form):
    """
    Validates user credentials submitted through a login form.

    Args:
        form (ImmutableMultiDict): The form data submitted via POST.

    Returns:
        tuple: (bool, str) where bool indicates success, and str is a flash message.
    """
    username = form.get("username", "").strip() ## making sure to strip leading and trailing characters, best way to compare username
    password = form.get("password", "")

    if not username or not password:
        return False, "Username and password are required."

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT password, role FROM users WHERE LOWER(username) = LOWER(%s)", (username,))
        result = cursor.fetchone()

        ## We have to start debugging what we actually got because its not allowing us to login
        # print(f"Result: {result}")
        # print(f"Result type: {type(result)}")
        # print(f"Result length: {len(result) if result else 'N/A'}")
        ## Problem was that MySQL was returning the results as dictionaries instead of tuples
    conn.close()

    if not result:
        return False, "Invalid username or password."

    ## To fix result to return the correct thing we have to give it a 'key' not an index, because dictionaries work with keys buddy
    #stored_hash = result[0]
    stored_hash = result['password']

    ## bcrypt requires bytes for hashing comparison
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        ## Password matches
        session['username'] = username
        session['role'] = result['role']
        return True, f"Welcome back, {username}!"
    else:
        return False, "Invalid username or password."
