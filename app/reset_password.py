"""
reset_password.py

Handles the password reset functionality via a secure tokenized route.

Key Features:
- Validates token authenticity, expiration, and usage.
- Ensures the new password is different from the previous one.
- Uses bcrypt to securely hash the updated password.
- Marks the reset token as used after successful reset.

Route:
- /reset_password/<token> (GET, POST)

Author: Emilio Vasquez
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .db import get_db_connection
import bcrypt
from datetime import datetime

reset_password_bp = Blueprint('reset_password', __name__)

@reset_password_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        # Step 1: Get the reset entry and validate it
        cursor.execute("""
            SELECT pr.user_id, pr.expires_at, pr.is_used, u.password
            FROM password_resets pr
            JOIN users u ON pr.user_id = u.id
            WHERE pr.token = %s
        """, (token,))
        entry = cursor.fetchone()

        if not entry:
            flash("Invalid or expired token.", "danger")
            return redirect(url_for('main.login'))

        if entry['is_used']:
            flash("This reset link has already been used.", "danger")
            return redirect(url_for('main.login'))

        if datetime.utcnow() > entry['expires_at']:
            flash("This reset link has expired.", "danger")
            return redirect(url_for('main.login'))

        user_id = entry['user_id']
        current_hashed_pw = entry['password']

    # Step 2: If POST, validate passwords
    if request.method == 'POST':
        new_pw = request.form.get('new_password')
        confirm_pw = request.form.get('confirm_password')

        if new_pw != confirm_pw:
            flash("Passwords do not match.", "danger")
            return render_template('reset_password.html', token=token)

        # Compare with old password (bcrypt)
        if bcrypt.checkpw(new_pw.encode('utf-8'), current_hashed_pw.encode('utf-8')):
            flash("New password must be different from the old one.", "danger")
            return render_template('reset_password.html', token=token)

        # Hash the new password (bcrypt)
        new_hashed_pw = bcrypt.hashpw(new_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Step 3: Update password and mark token as used
        with conn.cursor() as cursor:
            cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_hashed_pw, user_id))
            cursor.execute("UPDATE password_resets SET is_used = TRUE WHERE token = %s", (token,))
            conn.commit()

        conn.close()

        flash("Password reset successful. You can now log in.", "success")
        return redirect(url_for('main.login'))

    return render_template('reset_password.html', token=token)
