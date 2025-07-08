from app.db import get_db_connection
import json
import os

def migrate_test_cases():
    # Locate the JSON file
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')

    with open(file_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    conn = get_db_connection()
    with conn.cursor() as cursor:
        for q in questions:
            slug = q['slug']

            # Get question ID by slug
            cursor.execute("SELECT id FROM questions WHERE slug = %s", (slug,))
            result = cursor.fetchone()
            if not result:
                print(f"[SKIPPED] Question not found in DB: {slug}")
                continue

            question_id = result['id']
            test_cases = q.get('test_cases', [])

            for case in test_cases:
                input_data = case.get('input')
                expected_output = case.get('expected_output')
                description = case.get('description', '')
                setup_sql = None

                raw_setup = case.get('setup_sql')
                if isinstance(raw_setup, list):
                    setup_sql = "\n".join(raw_setup)
                elif isinstance(raw_setup, str):
                    setup_sql = raw_setup

                cursor.execute("""
                    INSERT INTO question_test_cases (question_id, description, input, expected_output, setup_sql)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    question_id,
                    description,
                    json.dumps(input_data) if input_data is not None else None,
                    json.dumps(expected_output) if expected_output is not None else None,
                    setup_sql
                ))

            print(f"[✓] Inserted {len(test_cases)} test case(s) for '{slug}'")

        conn.commit()
    conn.close()
    print("✅ Test cases migration complete.")

if __name__ == "__main__":
    migrate_test_cases()


## run on root: python -m app.scripts.migrate_test_cases