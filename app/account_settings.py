from flask import request, session, redirect, url_for, flash, render_template
from .db import get_db_connection
import bcrypt

def handle_account_settings():
    if 'username' not in session:
        flash("Please login to access account settings", "danger")
        return redirect(url_for('main.login'))

    # get user details
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, username, email, phone, password
            FROM users
            WHERE LOWER(username) = LOWER(%s)
        """, (session['username'],))
        user = cursor.fetchone()
    conn.close()

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('main.login'))

    # unpack from dictionary
    user_id = user['id']
    username = user['username']
    email = user['email']
    phone = user['phone']
    hashed_pw = user['password']

    ## handle POST
    if request.method == "POST":
        action = request.form.get("action")

        # change password
        if action == "change_password":
            current_password = request.form.get("current_password")
            new_password = request.form.get("new_password")
            confirm_new_password = request.form.get("confirm_new_password")

            if not bcrypt.checkpw(current_password.encode('utf-8'), hashed_pw.encode('utf-8')):
                flash("Current password is incorrect.", "danger")
            elif new_password != confirm_new_password:
                flash("New passwords do not match.", "danger")
            elif len(new_password) < 8:
                flash("New password must be at least 8 characters.", "danger")
            else:
                new_hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                conn = get_db_connection()
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE users SET password=%s WHERE id=%s
                    """, (new_hashed_pw, user_id))
                    conn.commit()
                conn.close()
                flash("Password updated successfully.", "success")
                return redirect(url_for('main.account_settings'))

        # update phone
        elif action == "update_phone":
            new_phone = request.form.get("phone").strip()
            if not new_phone:
                flash("Phone number cannot be empty.", "danger")
            else:
                conn = get_db_connection()
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE users SET phone=%s WHERE id=%s
                    """, (new_phone, user_id))
                    conn.commit()
                conn.close()
                flash("Phone number updated successfully.", "success")
                return redirect(url_for('main.account_settings'))

        # verify email placeholder
        elif action == "verify_email":
            flash("A verification email would be sent here (logic to implement).", "info")

    # render template always on GET or after POST
    return render_template(
        "account_settings.html",
        username=username,
        email=email,
        phone=phone if phone else ""
    )
