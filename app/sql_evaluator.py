import sqlite3

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

        # Setup: create and populate tables
        if setup_sql:
            if isinstance(setup_sql, str):
                cursor.executescript(setup_sql)
            elif isinstance(setup_sql, list):
                for statement in setup_sql:
                    cursor.execute(statement)

        # Run the user's query
        cursor.execute(user_query)
        results = cursor.fetchall()

        # Normalize both sides
        actual = normalize(results)
        expected = normalize(expected_output)

        if actual == expected:
            evaluation = "✅ Pass!"
        else:
            evaluation = f"❌ Fail. Expected: {expected} Got: {actual}"

        # Format output for display
        output = "\n".join(str(row) for row in results) if results else "(no rows returned)"
        MAX_LINES = 20
        lines = output.splitlines()
        displayed_output = "\n".join(lines[:MAX_LINES]) + ("\n...(truncated)..." if len(lines) > MAX_LINES else "")

        return evaluation, displayed_output

    except sqlite3.Error as e:
        return f"❌ SQL Error: {e}", "(no output)"

    finally:
        conn.close()