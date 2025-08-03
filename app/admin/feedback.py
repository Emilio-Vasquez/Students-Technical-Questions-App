# ------------------------------
# Feedback
# ------------------------------
import os
import mysql.connector
from flask import render_template
from app.admin.routes import admin_bp
from app.admin.utils import admin_required

@admin_bp.route('/feedback_inbox')
@admin_required
def feedback_inbox():
    # Local MySQL connection using env vars
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "your_username"),
        password=os.getenv("DB_PASSWORD", "your_password"),
        database=os.getenv("DB_NAME", "your_database"),
    )
    cursor = conn.cursor(dictionary=True)

    # Fetch all feedback entries
    cursor.execute("""
        SELECT 
            f.id,
            f.feedback_text AS message,
            f.created_at AS submitted_at,
            u.username
        FROM feedback f
        LEFT JOIN users u ON f.user_id = u.id
        ORDER BY f.created_at DESC
    """)
    feedback_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'admin/feedback_inbox.html',
        feedback_list=feedback_list
    )