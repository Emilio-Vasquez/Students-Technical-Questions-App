# ------------------------------
# Submissions
# ------------------------------
import os
import mysql.connector
from flask import render_template, request
from app.admin.routes import admin_bp
from app.admin.utils import admin_required

@admin_bp.route('/view_submissions')
@admin_required
def view_submissions():
    ## Local MySQL connection using env vars
    ## only necessary because dictionary=true was not working from get_db_connection()
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "your_username"),
        password=os.getenv("DB_PASSWORD", "your_password"),
        database=os.getenv("DB_NAME", "your_database"),
    )
    cursor = conn.cursor(dictionary=True)

    # Get optional filters
    username_filter = request.args.get('username')
    question_filter = request.args.get('question')
    sort_order = request.args.get('sort', 'desc')  # 'asc' or 'desc'

    # Validate sort_order
    if sort_order not in ['asc', 'desc']:
        sort_order = 'desc'

    # Base query
    base_query = """
        SELECT 
            s.id,
            s.code_submission AS code,
            s.passed,
            s.submitted_at,
            u.username,
            q.title AS question_title
        FROM user_submissions s
        JOIN users u ON s.user_id = u.id
        JOIN questions q ON s.question_slug = q.slug
    """

    # Conditions & parameters
    conditions = []
    params = []

    if username_filter:
        conditions.append("u.username = %s")
        params.append(username_filter)

    if question_filter:
        conditions.append("q.title LIKE %s")
        params.append(f"%{question_filter}%")

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    # Add sort order
    base_query += f" ORDER BY s.submitted_at {sort_order.upper()}"

    # Execute query
    cursor.execute(base_query, tuple(params))
    submissions = cursor.fetchall()

    # Fetch overall stats (unfiltered)
    cursor.execute("""
        SELECT 
            COUNT(*) AS total_submissions,
            SUM(CASE WHEN passed = 1 THEN 1 ELSE 0 END) AS total_passed,
            SUM(CASE WHEN passed = 0 THEN 1 ELSE 0 END) AS total_failed
        FROM user_submissions
    """)
    stats = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        'admin/view_submissions.html',
        submissions=submissions,
        stats=stats,
        username_filter=username_filter,
        question_filter=question_filter,
        sort_order=sort_order
    )