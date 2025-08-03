from flask import render_template, request, redirect, url_for, flash
from app.admin.routes import admin_bp
from app.admin.utils import admin_required
from app.db import get_db_connection

@admin_bp.route('/manage_test_cases/<int:question_id>', methods=['GET', 'POST'])
@admin_required
def manage_test_cases(question_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        # Fetch question title
        cursor.execute("SELECT id, title, language FROM questions WHERE id = %s", (question_id,))
        question = cursor.fetchone()
        if not question:
            flash("Question not found.", "danger")
            return redirect(url_for('admin.edit_question_list'))

        # Handle POST to add a new test case
        if request.method == 'POST':
            description = request.form.get('description')
            input_data = request.form.get('input')
            expected_output = request.form.get('expected_output')
            setup_sql = request.form.get('setup_sql') or None

            cursor.execute("""
                INSERT INTO question_test_cases (question_id, description, input, expected_output, setup_sql)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                question_id,
                description,
                input_data,
                expected_output,
                setup_sql
            ))
            conn.commit()
            flash("Test case added!", "success")
            return redirect(url_for('admin.manage_test_cases', question_id=question_id))

        # Fetch all test cases for this question
        cursor.execute("""
            SELECT id, description, input, expected_output, setup_sql
            FROM question_test_cases
            WHERE question_id = %s
            ORDER BY id ASC
        """, (question_id,))
        test_cases = cursor.fetchall()
    conn.close()

    return render_template(
        'admin/manage_test_cases.html',
        question=question,
        test_cases=test_cases
    )

