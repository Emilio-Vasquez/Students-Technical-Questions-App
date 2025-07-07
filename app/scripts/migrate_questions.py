from app.db import get_db_connection
import json
import os

def migrate_questions():
    # locate the JSON file
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')

    # load JSON questions
    with open(file_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    conn = get_db_connection()
    with conn.cursor() as cursor:
        for q in questions:
            # optionally check if it already exists to avoid duplicates
            cursor.execute("""
                SELECT id FROM questions WHERE slug=%s
            """, (q['slug'],))
            existing = cursor.fetchone()
            if existing:
                print(f"Skipping existing question: {q['slug']}")
                continue

            # Normalize setup_sql to a string
            raw_setup = q.get('setup_sql')
            if isinstance(raw_setup, list):
                setup_sql = "\n".join(raw_setup)
            elif isinstance(raw_setup, str):
                setup_sql = raw_setup
            else:
                setup_sql = None

            cursor.execute("""
                INSERT INTO questions (title, slug, prompt, expected_output, category, language, setup_sql)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                q['title'],
                q['slug'],
                q['prompt'],
                q['expected_output'],
                q.get('category'),
                q.get('language'),
                setup_sql
            ))

        conn.commit()
    conn.close()
    print("Migration completed!")

if __name__ == "__main__":
    migrate_questions()