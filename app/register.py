from .db import get_db_connection
import bcrypt
import re

"""
Okay, so first off, the javascript already informs the user of what is acceptable
and what is not. But what it doesn't do, is it doesn't prevent the user from submitting
the incorrect things. So even if it does warn them, it doesn't stop them.
This is where the back-end comes into play, if the user doesn't input the correct thing,
in order to stop them from submitting it to us, we have to handle that in our back-end.
"""

def handle_registration(form):
    username = form.get("username", "").strip()
    email = form.get("email", "").strip()
    password = form.get("password", "").strip()
    confirm_password = form.get("confirm_password", "").strip()

    ## These are the pre-requisites outlined from our javascript:
    if len(username) < 4:
        return False, "Username must be at least 4 characters."
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
    if not re.match(email_regex, email): ## This is a more complex check to validate email, not the best, but a middle ground I guess
        return False, "Invalid email format."
    
    ## Password is more complex:
    ## Password complexity rules:
    if len(password) < 8:
        return False, "Password must be at least 8 characters."

    ## At least one uppercase letter
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."

    ## At least one lowercase letter
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."

    ## At least one digit
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."

    ## At least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."

    ## No spaces
    if re.search(r"\s", password):
        return False, "Password cannot contain spaces."
    
    ## Check if the passwords match or not
    if password != confirm_password:
        return False, "Passwords do not match."

    ## first check db for existing user
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE username=%s OR email=%s", (username, email))
        existing = cursor.fetchone()
        if existing:
            return False, "Username or email already in use."

        ## hash password
        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        ## insert new user
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_pw)
        )
        conn.commit()
    conn.close()
    return True, "User registered."
