from flask import Blueprint, request, redirect, url_for, flash, session
from .db import get_db_connection

comment_bp = Blueprint("comment", __name__)

@comment_bp.route('/post_comment/<int:question_id>', methods=["POST"])
def post_comment(question_id):
    if 'username' not in session:
        flash("You must be logged in to comment.", "warning")
        return redirect(url_for("main.question_detail", slug=request.form.get("slug")))

    parent_id = request.form.get("parent_id")
    if parent_id == "":
        parent_id = None  # None if it's a top-level comment
    content = request.form.get("content", "").strip()
    slug = request.form.get("slug")  # Needed to redirect back

    if not content:
        flash("Comment cannot be empty.", "danger")
        return redirect(url_for("main.question_detail", slug=slug))

    conn = get_db_connection()
    with conn.cursor() as cursor:
        # Get user_id
        cursor.execute("SELECT id FROM users WHERE username = %s", (session["username"],))
        user = cursor.fetchone()
        if not user:
            flash("User not found.", "danger")
            return redirect(url_for("main.question_detail", slug=slug))

        cursor.execute("""
            INSERT INTO comments (question_id, user_id, parent_id, content)
            VALUES (%s, %s, %s, %s)
        """, (question_id, user["id"], parent_id or None, content))
        conn.commit()
    conn.close()

    return redirect(url_for("main.question_detail", slug=slug))