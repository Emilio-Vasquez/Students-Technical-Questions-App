from flask import Blueprint, request, redirect, url_for, flash, jsonify, session
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
            SELECT c.id, c.content, c.created_at, c.parent_id, u.username, u.role
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

def vote_on_comment():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.get_json()
    comment_id = data.get('comment_id')
    vote_value = data.get('vote')  # +1 or -1

    if vote_value not in [-1, 1]:
        return jsonify({'error': 'Invalid vote'}), 400

    # Look up user_id using username
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
        user_row = cursor.fetchone()

        if not user_row:
            return jsonify({'error': 'User not found'}), 404

        user_id = user_row['id']

        # Upsert vote
        cursor.execute("""
            INSERT INTO comment_votes (user_id, comment_id, vote)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE vote = VALUES(vote)
        """, (user_id, comment_id, vote_value))
        conn.commit()

        # Recalculate total score
        cursor.execute("""
            SELECT SUM(vote) as score FROM comment_votes WHERE comment_id = %s
        """, (comment_id,))
        result = cursor.fetchone()
        score = result['score'] if result['score'] is not None else 0

    return jsonify({'score': max(score, 0), 'true_score': score})

# Example: assuming you're loading comments for a question
def get_comments_with_scores(question_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT c.id, COALESCE(SUM(v.vote), 0) AS score
            FROM comments c
            LEFT JOIN comment_votes v ON c.id = v.comment_id
            WHERE c.question_id = %s
            GROUP BY c.id
        """, (question_id,))
        rows = cursor.fetchall()
    conn.close()
    return {row["id"]: row["score"] for row in rows}