from flask import request, session, redirect, url_for, flash, render_template
from .db import get_db_connection
import bcrypt
import random
import string
from datetime import datetime, timedelta
from flask_mail import Message
from .mailer import mail

def handle_account_settings():
    if 'username' not in session:
        flash("Please login to access account settings", "danger")
        return redirect(url_for('main.login'))

    conn = get_db_connection()
    with conn.cursor() as cursor:
        # get user details
        cursor.execute("""
            SELECT id, username, email, phone, password, is_verified
            FROM users
            WHERE LOWER(username) = LOWER(%s)
        """, (session['username'],))
        user = cursor.fetchone()
        is_verified = bool(user.get("is_verified", False))

        if not user:
            conn.close()
            flash("User not found.", "danger")
            return redirect(url_for('main.login'))

        user_id = user['id']

        # get progress counts + total counts in one go
        cursor.execute("""
            SELECT
                SUM(CASE WHEN q.category = 'Computer Science' AND us.passed = 1 THEN 1 ELSE 0 END) as cs_completed,
                SUM(CASE WHEN q.category = 'Data Science' AND us.passed = 1 THEN 1 ELSE 0 END) as ds_completed,
                SUM(CASE WHEN q.category = 'Databases' AND us.passed = 1 THEN 1 ELSE 0 END) as db_completed,
                SUM(CASE WHEN q.category = 'Computer Science' THEN 1 ELSE 0 END) as cs_total,
                SUM(CASE WHEN q.category = 'Data Science' THEN 1 ELSE 0 END) as ds_total,
                SUM(CASE WHEN q.category = 'Databases' THEN 1 ELSE 0 END) as db_total
            FROM questions q
            LEFT JOIN user_submissions us
            ON us.question_slug = q.slug AND us.user_id = %s
        """, (user_id,))
        progress_row = cursor.fetchone()

    conn.close()

    progress = {
        "cs_completed": progress_row["cs_completed"] or 0,
        "ds_completed": progress_row["ds_completed"] or 0,
        "db_completed": progress_row["db_completed"] or 0
    }
    totals = {
        "cs": progress_row["cs_total"] or 0,
        "ds": progress_row["ds_total"] or 0,
        "db": progress_row["db_total"] or 0
    }

    # handle POST
    if request.method == "POST":
        action = request.form.get("action")

        if action == "change_password":
            current_password = request.form.get("current_password")
            new_password = request.form.get("new_password")
            confirm_new_password = request.form.get("confirm_new_password")

            if not bcrypt.checkpw(current_password.encode('utf-8'), user['password'].encode('utf-8')):
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

        elif action == "verify_email":
            verification_code = ''.join(random.choices(string.digits, k=6))
            expires_at = datetime.utcnow() + timedelta(minutes=10)

            conn = get_db_connection()
            with conn.cursor() as cursor:
                # Invalidate any previous unused codes
                cursor.execute("""
                    UPDATE email_verifications
                    SET is_used = TRUE
                    WHERE user_id = %s AND is_used = FALSE
                """, (user_id,))

                # Insert new verification record
                cursor.execute("""
                    INSERT INTO email_verifications (user_id, verification_code, expires_at)
                    VALUES (%s, %s, %s)
                """, (user_id, verification_code, expires_at))
                conn.commit()

            # Send the verification email
            msg = Message("Verify your email",
                        recipients=[user["email"]])
            msg.body = f"""Hi {user['username']},

        Here is your verification code: {verification_code}

        It will expire in 10 minutes.

        If you didn’t request this, you can ignore it.
        """
            mail.send(msg)

            flash("Verification code sent to your email.", "success")
            conn.close()
            return redirect(url_for('main.account_settings'))
        
        elif action == "submit_verification_code":
            code_entered = request.form.get("verification_code").strip()

            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id FROM email_verifications
                    WHERE user_id = %s AND verification_code = %s
                    AND is_used = FALSE AND expires_at > NOW()
                """, (user_id, code_entered))
                row = cursor.fetchone()

                if row:
                    cursor.execute("""
                        UPDATE users SET is_verified = TRUE WHERE id = %s
                    """, (user_id,))
                    cursor.execute("""
                        UPDATE email_verifications SET is_used = TRUE WHERE id = %s
                    """, (row["id"],))
                    conn.commit()
                    flash("Your email has been successfully verified!", "success")
                else:
                    flash("Invalid or expired verification code.", "danger")

            conn.close()
            return redirect(url_for('main.account_settings'))


    return render_template(
        "account_settings.html",
        username=user["username"],
        email=user["email"],
        phone=user["phone"] if user["phone"] else "",
        progress=progress,
        totals=totals,
        is_verified=is_verified
    )
