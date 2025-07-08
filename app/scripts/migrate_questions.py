from app.db import get_db_connection
import json
import os

def migrate_questions():
    # Locate the JSON file
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')

    # Load JSON questions
    with open(file_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    conn = get_db_connection()
    with conn.cursor() as cursor:
        for q in questions:
            # Check if question already exists
            cursor.execute("SELECT id FROM questions WHERE slug = %s", (q['slug'],))
            if cursor.fetchone():
                print(f"⏩ Skipping existing question: {q['slug']}")
                continue

            # Normalize setup_sql to a string
            raw_setup = q.get('setup_sql')
            if isinstance(raw_setup, list):
                setup_sql = "\n".join(raw_setup)
            elif isinstance(raw_setup, str):
                setup_sql = raw_setup
            else:
                setup_sql = None

            # Insert new question
            cursor.execute("""
                INSERT INTO questions (title, slug, prompt, category, language, setup_sql, function_signature)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                q['title'],
                q['slug'],
                q['prompt'],
                q.get('category'),
                q.get('language'),
                setup_sql,
                q.get('function_signature')  # May be None for SQL
            ))

        conn.commit()
    conn.close()
    print("✅ Questions migration complete.")

if __name__ == "__main__":
    migrate_questions()
    
## To run this migration run this at the root of the project: python -m app.scripts.migrate_questions