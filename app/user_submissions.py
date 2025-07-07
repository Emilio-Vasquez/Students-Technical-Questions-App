from .db import get_db_connection

def store_user_submission(username, slug, answer, language, passed):
    """
    Stores or updates a user's submission for a question.

    Args:
        username (str): the username from session
        slug (str): question slug
        answer (str): their submitted code
        language (str): python or sql
        passed (bool): whether it passed
    """
    conn = get_db_connection()
    with conn.cursor() as cursor:
        # get user id
        cursor.execute("""
            SELECT id FROM users WHERE LOWER(username) = LOWER(%s)
        """, (username,))
        user_row = cursor.fetchone()
        if user_row:
            user_id = user_row['id']
            # check if record exists
            cursor.execute("""
                SELECT id FROM user_submissions
                WHERE user_id=%s AND question_slug=%s
            """, (user_id, slug))
            existing = cursor.fetchone()
            if existing:
                # update
                cursor.execute("""
                    UPDATE user_submissions
                    SET code_submission=%s, language=%s, passed=%s
                    WHERE user_id=%s AND question_slug=%s
                """, (answer, language, passed, user_id, slug))
            else:
                # insert
                cursor.execute("""
                    INSERT INTO user_submissions
                    (user_id, question_slug, code_submission, language, passed)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, slug, answer, language, passed))
            conn.commit()
    conn.close()
