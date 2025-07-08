import sqlite3
import time
import ast

def evaluate_sql(user_query, expected_output, setup_sql=None):
    """
    Evaluates a user's SQL query against expected output.
    
    Parameters:
        user_query (str): SQL query submitted by user.
        expected_output (list of tuple): Expected result set (e.g., [(1000,), (2000,)])
        setup_sql (list of str): List of SQL statements to create/populate tables.
        
    Returns:
        (evaluation_str, output_str): Result of evaluation and user-visible output.
    """
    def normalize(value):
        """
        Normalize nested results to a comparable scalar or list of scalars.
        Convert all scalars to strings for type-agnostic comparison.
        """
        if isinstance(value, list) and len(value) == 1:
            return normalize(value[0])
        if isinstance(value, tuple) and len(value) == 1:
            return normalize(value[0])
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, (list, tuple)):
            return [normalize(v) for v in value]
        return str(value)

    try:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()

        if setup_sql:
            if isinstance(setup_sql, str):
                cursor.executescript(setup_sql)
            elif isinstance(setup_sql, list):
                for statement in setup_sql:
                    cursor.execute(statement)

        start_time = time.perf_counter()  # Start timer
        cursor.execute(user_query)
        results = cursor.fetchall()
        end_time = time.perf_counter()  # End timer
        elapsed_time = round((end_time - start_time) * 1000, 2)  # changing it into milliseconds

        actual = normalize(results)
        try:
            parsed_expected = ast.literal_eval(expected_output) if isinstance(expected_output, str) else expected_output
        except Exception as e:
            return f"❌ Invalid expected_output format: {e}", "(no output)"

        expected = normalize(parsed_expected)

        if actual == expected:
            evaluation = "✅ Pass!"
        else:
            evaluation = f"❌ Fail. Expected: {expected} Got: {actual}"

        output = "\n".join(str(row) for row in results) if results else "(no rows returned)"
        lines = output.splitlines()
        displayed_output = "\n".join(lines[:20]) + ("\n...(truncated)..." if len(lines) > 20 else "")

        evaluation += f" (⏱ {elapsed_time} ms)"
        return evaluation, displayed_output

    except sqlite3.Error as e:
        return f"❌ SQL Error: {e}", "(no output)"

    finally:
        conn.close()