from app.db import get_db_connection
import json
import os

def migrate_questions():
    # locate the JSON file
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')

    # load JSON questions
    with open(file_path, 'r') as f:
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

            # insert new question
            cursor.execute("""
                INSERT INTO questions (title, slug, prompt, expected_output, category, language)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                q['title'],
                q['slug'],
                q['prompt'],
                q['expected_output'],
                q['category'],
                q['language']
            ))
        conn.commit()
    conn.close()
    print("Migration completed!")

if __name__ == "__main__":
    migrate_questions()

## To run this migration run this at the root of the project: python -m app.scripts.migrate_questions