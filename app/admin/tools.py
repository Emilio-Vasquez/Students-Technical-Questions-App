# ------------------------------
# System Tools
# ------------------------------
import csv
import os
import mysql.connector
from flask import request, Response, flash, redirect, url_for, render_template
from app.admin.routes import admin_bp
from app.admin.utils import superadmin_required
from app.db import get_db_connection

@admin_bp.route('/system_tools')
@superadmin_required
def system_tools():
    return render_template('admin/tools.html')

@admin_bp.route('/manage_submissions')
@superadmin_required
def manage_submissions():
    conn = get_db_connection()
    cursor = conn.cursor()

    username_filter = request.args.get('username')
    question_filter = request.args.get('question')
    sort_order = request.args.get('sort', 'desc')
    if sort_order not in ['asc', 'desc']:
        sort_order = 'desc'

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

    base_query += f" ORDER BY s.submitted_at {sort_order.upper()}"

    cursor.execute(base_query, tuple(params))
    submissions = cursor.fetchall()

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
        'admin/manage_submissions.html',
        submissions=submissions,
        stats=stats,
        username_filter=username_filter,
        question_filter=question_filter,
        sort_order=sort_order
    )

@admin_bp.route('/edit_submission/<int:submission_id>', methods=['GET', 'POST'])
@superadmin_required
def edit_submission(submission_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        new_code = request.form.get('code', '').strip()
        new_passed = request.form.get('passed', '0') == '1'

        try:
            cursor.execute("""
                UPDATE user_submissions
                SET code_submission = %s, passed = %s
                WHERE id = %s
            """, (new_code, new_passed, submission_id))
            conn.commit()
            flash("Submission updated successfully.")
            return redirect(url_for('admin.manage_submissions'))
        except Exception as e:
            conn.rollback()
            flash(f"Failed to update submission: {str(e)}")

    cursor.execute("""
        SELECT s.id, s.code_submission AS code, s.passed, u.username, q.title AS question_title
        FROM user_submissions s
        JOIN users u ON s.user_id = u.id
        JOIN questions q ON s.question_slug = q.slug
        WHERE s.id = %s
    """, (submission_id,))
    submission = cursor.fetchone()

    cursor.close()
    conn.close()

    if not submission:
        flash("Submission not found.")
        return redirect(url_for('admin.manage_submissions'))

    return render_template('admin/edit_submission.html', submission=submission)

@admin_bp.route('/reset_submissions', methods=['POST'])
@superadmin_required
def reset_submissions():
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM user_submissions")
        db.commit()
        flash("All user submissions have been reset.")
    except Exception as e:
        db.rollback()
        flash(f"Failed to reset submissions: {str(e)}")
    finally:
        cursor.close()
        db.close()
    return redirect(url_for('admin.system_tools'))

@admin_bp.route('/export_data')
@superadmin_required
def export_data():
    username = request.args.get('username')
    question_title = request.args.get('question_title')

    db = get_db_connection()
    cursor = db.cursor()

    query = """
        SELECT s.id, s.username, q.title AS question_title, s.submission_code, 
               s.result, s.passed, s.submitted_at
        FROM user_submissions s
        JOIN questions q ON s.question_id = q.id
        WHERE 1=1
    """
    params = []

    if username:
        query += " AND s.username = %s"
        params.append(username)

    if question_title:
        query += " AND q.title LIKE %s"
        params.append(f"%{question_title}%")

    query += " ORDER BY s.submitted_at DESC"

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    cursor.close()
    db.close()

    def generate():
        data = csv.StringIO()
        writer = csv.writer(data)
        writer.writerow(['ID', 'Username', 'Question', 'Code', 'Result', 'Passed', 'Submitted At'])
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        for row in rows:
            writer.writerow([
                row['id'], row['username'], row['question_title'],
                row['submission_code'], row['result'], row['passed'], row['submitted_at']
            ])
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    return Response(generate(), mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment; filename=submissions_export.csv'})

@admin_bp.route('/delete_submissions', methods=['POST'])
@superadmin_required
def delete_submissions():
    submission_ids = request.form.get('submission_ids', '')
    if not submission_ids:
        flash("No submissions selected for deletion.")
        return redirect(url_for('admin.system_tools'))

    ids = [id.strip() for id in submission_ids.split(',') if id.strip().isdigit()]
    if not ids:
        flash("Invalid submission ID format.")
        return redirect(url_for('admin.system_tools'))

    db = get_db_connection()
    cursor = db.cursor()

    try:
        format_strings = ','.join(['%s'] * len(ids))
        cursor.execute(f"DELETE FROM user_submissions WHERE id IN ({format_strings})", tuple(ids))
        db.commit()
        flash(f"{len(ids)} submission(s) deleted.")
    except Exception as e:
        db.rollback()
        flash(f"Error deleting submissions: {str(e)}")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('admin.system_tools'))
