import sqlite3
import time
import json

def normalize(value):
    """Normalize nested results for type-agnostic comparison."""
    if isinstance(value, list) and len(value) == 1:
        return normalize(value[0])
    if isinstance(value, tuple) and len(value) == 1:
        return normalize(value[0])
    if isinstance(value, (int, float)):
        return round(float(value), 4)  # Normalize all numbers as float
    if isinstance(value, (list, tuple)):
        return [normalize(v) for v in value]
    return str(value).strip()

def evaluate_sql(user_query, expected_output, setup_sql=None):
    """
    Evaluates a SQL query against a set of test cases.
    Each test case may contain:
        - setup_sql: list or string of SQL setup statements
        - expected_output: list of rows (list of tuples or lists)
        - description: optional label
    """
    if isinstance(setup_sql, str):
        setup_sql = [stmt.strip() for stmt in setup_sql.split(";") if stmt.strip()]
    elif not setup_sql:
        setup_sql = []

    error = ""
    output_rows = []
    elapsed = 0

    try:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()

        for stmt in setup_sql:
            if stmt.strip():
                cursor.execute(stmt)

        start_time = time.perf_counter()
        cursor.execute(user_query)
        output_rows = cursor.fetchall()
        end_time = time.perf_counter()
        elapsed = round((end_time - start_time) * 1000, 2)

        normalized_output = normalize(output_rows)
        normalized_expected = normalize(expected_output)
        passed = normalized_output == normalized_expected

    except sqlite3.Error as e:
        error = str(e)
        passed = False

    finally:
        conn.close()

    result = f"✅ Passed ({elapsed} ms)" if passed else f"❌ Failed ({elapsed} ms), {error or 'Output mismatch'}"
    return result, output_rows