from flask import Blueprint, request, redirect, url_for, flash, session
from .db import get_db_connection
from collections import defaultdict


comment_bp = Blueprint("comment", __name__)

def build_comment_tree(flat_comments):
    comment_dict = {comment['id']: comment for comment in flat_comments}
    children_map = defaultdict(list)

    for comment in flat_comments:
        parent_id = comment['parent_id']
        if parent_id:
            children_map[parent_id].append(comment)

    def count_descendants(comment_id):
        children = children_map.get(comment_id, [])
        total = len(children)
        for child in children:
            total += count_descendants(child['id'])
        return total

    # Attach replies and count recursively
    for comment in flat_comments:
        comment['replies'] = children_map.get(comment['id'], [])
        comment['reply_count'] = count_descendants(comment['id'])

    return [comment for comment in flat_comments if comment['parent_id'] is None]

def get_all_comments(question_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT c.id, c.content, c.created_at, c.parent_id, u.username
            FROM comments c
            LEFT JOIN users u ON c.user_id = u.id
            WHERE c.question_id = %s
            ORDER BY c.created_at ASC
        """, (question_id,))
        return cursor.fetchall()

@comment_bp.route('/post_comment/<int:question_id>', methods=["POST"])
def post_comment(question_id):
    if 'username' not in session:
        flash("You must be logged in to comment.", "warning")
        return redirect(url_for("main.question_detail", slug=request.form.get("slug")))

    parent_id = request.form.get("parent_id") or None
    content = request.form.get("content", "").strip()
    slug = request.form.get("slug")

    if not content:
        flash("Comment cannot be empty.", "danger")
        return redirect(url_for("main.question_detail", slug=slug))

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE username = %s", (session["username"],))
        user = cursor.fetchone()
        if not user:
            flash("User not found.", "danger")
            return redirect(url_for("main.question_detail", slug=slug))

        cursor.execute("""
            INSERT INTO comments (question_id, user_id, parent_id, content)
            VALUES (%s, %s, %s, %s)
        """, (question_id, user["id"], parent_id, content))
        conn.commit()
    conn.close()

    return redirect(url_for("main.question_detail", slug=slug))