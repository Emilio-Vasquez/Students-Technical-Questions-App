# app/forgot_password.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .db import get_db_connection
from .mailer import mail
from flask_mail import Message
import string, random
from datetime import datetime, timedelta

forgot_password_bp = Blueprint('forgot_password', __name__)

@forgot_password_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email').strip()

        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Find user by username or email
            cursor.execute("""
                SELECT id, email, username FROM users
                WHERE username = %s OR email = %s
            """, (username_or_email, username_or_email))
            user = cursor.fetchone()

            if not user:
                flash("No account found with that username or email.", "danger")
                return redirect(url_for('forgot_password.forgot_password'))

            # Generate token
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=48))
            expires_at = datetime.utcnow() + timedelta(hours=1)

            # Save token
            cursor.execute("""
                INSERT INTO password_resets (user_id, token, expires_at)
                VALUES (%s, %s, %s)
            """, (user['id'], token, expires_at))
            conn.commit()

        conn.close()

        # Send email
        reset_url = url_for('reset_password.reset_password', token=token, _external=True)
        msg = Message("Password Reset Request",
                      recipients=[user['email']])
        msg.body = f"""Hi {user['username']},

You requested to reset your password.

Click the link below to reset it:
{reset_url}

This link will expire in 1 hour.

If you didn't request this, you can ignore this email.
"""
        mail.send(msg)

        flash("A password reset link has been sent to your email.", "success")
        return redirect(url_for('main.login'))

    return render_template("forgot_password.html")
