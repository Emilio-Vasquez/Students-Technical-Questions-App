import sqlite3

def evaluate_sql(user_query, expected_output):
    try:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        ## preload schema
        ## IMPORTANT: These two codes below essentially create a table called sales to be used to evaluate
        ## whether the evaulator work or not!
        ## We need to create a db later and make sure to connect it, and based on the question pick the result to compare
        # Setup test table, adjust for real later
        cursor.execute("CREATE TABLE sales (amount INT);")
        cursor.executemany("INSERT INTO sales(amount) VALUES (?)", [(400,), (600,)])

        cursor.execute(user_query)
        results = cursor.fetchall()

        # Flatten results for simpler display
        output = "\n".join(str(row) for row in results) if results else "(no rows returned)"

        # expected_output is assumed string, you could parse it better
        if str(results) == expected_output:
            evaluation = "✅ Pass!"
        else:
            evaluation = f"❌ Fail: Output does not match expected."

        # limit output lines
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
