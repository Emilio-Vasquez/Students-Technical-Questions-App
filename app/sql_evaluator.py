import sqlite3

def evaluate_sql(user_query, expected_output):
    try:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        # Setup demo table
        cursor.execute("CREATE TABLE sales (amount INT);")
        cursor.executemany("INSERT INTO sales(amount) VALUES (?)", [(400,), (600,)])

        # run user code
        cursor.execute(user_query)
        results = cursor.fetchall()

        # evaluation based on first column of first row
        if results and str(results[0][0]) == expected_output:
            evaluation = "✅ Pass!"
        else:
            evaluation = f"❌ Fail. Got: {results[0][0] if results else 'NULL'}, Expected: {expected_output}"

        # pretty output for user to see
        output = "\n".join(str(row) for row in results) if results else "(no rows returned)"
        MAX_OUTPUT_LINES = 20
        output_lines = output.splitlines()
        if len(output_lines) > MAX_OUTPUT_LINES:
            displayed_output = "\n".join(output_lines[:MAX_OUTPUT_LINES]) + "\n...(truncated)..."
        else:
            displayed_output = output

        return evaluation, displayed_output

    except sqlite3.Error as e:
        return f"❌ SQL Error: {e}", "(no output)"
    finally:
        conn.close()