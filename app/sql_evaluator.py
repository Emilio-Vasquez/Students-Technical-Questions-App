import sqlite3

def evaluate_sql(user_query, expected_output):
    try:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        ## preload schema
        ## IMPORTANT: These two codes below essentially create a table called sales to be used to evaluate
        ## whether the evaulator work or not!
        ## We need to create a db later and make sure to connect it, and based on the question pick the result to compare
        cursor.execute("CREATE TABLE sales (amount INT);")
        cursor.executemany("INSERT INTO sales(amount) VALUES (?)", [(400,), (600,)])

        ## run user query
        cursor.execute(user_query)
        result = cursor.fetchone()

        if result and str(result[0]) == expected_output:
            return "✅ Pass!"
        else:
            return f"❌ Fail. Got: {result[0] if result else 'NULL'}, Expected: {expected_output}"
    except sqlite3.Error as e:
        return f"SQL Error: {e}"
    finally:
        conn.close()
