# ------------------------------
# Question Management
# ------------------------------
import re
from flask import render_template, request, redirect, url_for, flash
from app.admin.routes import admin_bp
from app.admin.utils import admin_required
from app.db import get_db_connection

def generate_slug(title):
    slug = title.lower()
    slug = re.sub(r'[\W_]+', '-', slug)  # Replace non-word chars with dashes
    slug = slug.strip('-')
    return slug

@admin_bp.route('/add_question', methods=['GET', 'POST'])
@admin_required
def add_question():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        prompt = request.form.get('prompt', '').strip()
        difficulty = request.form.get('difficulty')
        category = request.form.get('category')
        language = request.form.get('language')

        # Validation: All fields required
        if not all([title, prompt, difficulty, category, language]):
            flash("All fields are required.", "danger")
            return redirect(url_for('admin.add_question'))

        # Validation: Acceptable categories and languages
        allowed_categories = {"Computer Science", "Databases"}
        allowed_languages = {"python", "sql"}

        if category not in allowed_categories or language not in allowed_languages:
            flash("Invalid category or language selected.", "danger")
            return redirect(url_for('admin.add_question'))

        # Generate slug and validate format
        slug = generate_slug(title)
        if not slug or len(slug) < 3:
            flash("Generated slug is too short or invalid. Please check the title.", "danger")
            return redirect(url_for('admin.add_question'))

        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Check for duplicate slug
            cursor.execute("SELECT id FROM questions WHERE slug = %s", (slug,))
            if cursor.fetchone():
                flash("A question with a similar title already exists. Please choose a different title.", "danger")
                return redirect(url_for('admin.edit_question', question_id=question_id))

            # Insert new question
            cursor.execute("""
                INSERT INTO questions (title, prompt, slug, difficulty, category, language)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (title, prompt, slug, difficulty, category, language))

            question_id = cursor.lastrowid
            conn.commit()
        conn.close()

        flash("Question added successfully!", "success")
        # Redirect to test case manager
        return redirect(url_for('admin.manage_test_cases', question_id=question_id))

    return render_template('admin/add_question.html')

@admin_bp.route('/edit_question/<int:question_id>', methods=['GET', 'POST'])
@admin_required
def edit_question(question_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        # Get current question
        cursor.execute("SELECT * FROM questions WHERE id = %s", (question_id,))
        question = cursor.fetchone()
        if not question:
            flash("Question not found.", "danger")
            return redirect(url_for('admin.edit_question_list'))

        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            prompt = request.form.get('prompt', '').strip()
            difficulty = request.form.get('difficulty')
            category = request.form.get('category')
            language = request.form.get('language')
            function_signature = request.form.get('function_signature') or None

            # Optional: regenerate slug
            from app.admin.questions import generate_slug
            slug = generate_slug(title)

            # Update the question
            cursor.execute("""
                UPDATE questions
                SET title=%s, prompt=%s, slug=%s, difficulty=%s,
                    category=%s, language=%s, function_signature=%s
                WHERE id=%s
            """, (
                title, prompt, slug, difficulty,
                category, language, function_signature,
                question_id
            ))
            conn.commit()
            flash("Question updated successfully!", "success")
            return redirect(url_for('admin.edit_question_list'))

    conn.close()
    return render_template('admin/edit_question.html', question=question)

@admin_bp.route('/edit_question_list')
@admin_required
def edit_question_list():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, title, slug, difficulty, category
            FROM questions
            ORDER BY id DESC
        """)
        questions = cursor.fetchall()
    conn.close()

    return render_template('admin/edit_question_list.html', questions=questions)
  
@admin_bp.route('/delete_question/<int:question_id>', methods=['POST'])
@admin_required
def delete_question(question_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        # Optional: delete associated test cases
        cursor.execute("DELETE FROM question_test_cases WHERE question_id = %s", (question_id,))
        
        # Delete the question
        cursor.execute("DELETE FROM questions WHERE id = %s", (question_id,))
        conn.commit()

    conn.close()
    flash("Question deleted successfully.", "success")
    return redirect(url_for('admin.edit_question_list'))
