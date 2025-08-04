# ------------------------------
# Feedback
# ------------------------------
import os
import math
import mysql.connector
from flask import render_template, request
from app.admin.routes import admin_bp
from app.admin.utils import admin_required
from app.db import get_db_connection
from datetime import date
import datetime

@admin_bp.route('/feedback_inbox')
@admin_required
def feedback_inbox():
    # Pagination & Filters
    page = int(request.args.get('page', 1))
    per_page = 50
    offset = (page - 1) * per_page

    username_filter = request.args.get('username', '').strip()
    category_filter = request.args.get('category', '').strip()
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()

    # DB connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # Build WHERE clauses
    filters = []
    values = []
    if username_filter:
        filters.append("(u.username LIKE %s OR f.name LIKE %s)")
        values.extend([f"%{username_filter}%", f"%{username_filter}%"])
    if category_filter:
        filters.append("f.category = %s")
        values.append(category_filter)
    if start_date:
        filters.append("f.created_at >= %s")
        values.append(start_date)
    if end_date:
      try:
          parsed_end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
          end_of_day = parsed_end.replace(hour=23, minute=59, second=59)
          filters.append("f.created_at <= %s")
          values.append(end_of_day)
      except ValueError:
          pass

    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

    # Total count for pagination
    count_query = f"""
        SELECT COUNT(*) as total
        FROM feedback f
        LEFT JOIN users u ON f.user_id = u.id
        {where_clause}
    """
    cursor.execute(count_query, tuple(values))
    total_feedback = cursor.fetchone()['total']
    total_pages = math.ceil(total_feedback / per_page)

    # Fetch paginated results
    query = f"""
        SELECT 
            f.id,
            f.feedback_text AS message,
            f.created_at AS submitted_at,
            COALESCE(u.username, f.name) AS user_display_name
        FROM feedback f
        LEFT JOIN users u ON f.user_id = u.id
        {where_clause}
        ORDER BY f.created_at DESC
        LIMIT %s OFFSET %s
    """
    cursor.execute(query, tuple(values + [per_page, offset]))
    feedback_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'admin/feedback_inbox.html',
        feedback_list=feedback_list,
        current_page=page,
        total_pages=total_pages,
        username_filter=username_filter,
        category_filter=category_filter,
        start_date=start_date,
        end_date=end_date,
        today=date.today().isoformat()
    )
