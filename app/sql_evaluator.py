"""
SQL evaluation utility for comparing user-submitted queries to expected outputs.

This module executes SQL against a temporary in-memory SQLite database.
It supports normalization of outputs for flexible comparison and measures query performance.
"""
import sqlite3
import time
import json

def normalize(value):
    """
    Recursively normalize SQL output for comparison.

    - Converts all numeric values to rounded floats (4 decimal places).
    - Strips strings of whitespace.
    - Flattens single-element lists/tuples.
    - Ensures consistent data type representation for comparison.

    Args:
        value (any): A nested list, tuple, int, float, or string.

    Returns:
        any: Normalized representation (typically list of strings or floats).
    """
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
    Executes a SQL query and compares the output to expected results.

    Args:
        user_query (str): The user's SQL query to evaluate.
        expected_output (list): The expected output rows (as list of tuples or lists).
        setup_sql (str or list, optional): SQL setup statements (e.g., CREATE TABLE, INSERTs)
                                           provided as a single string or list of strings.

    Returns:
        tuple:
            - result_msg (str): Pass/fail message including execution time or error reason.
            - output_rows (list): Raw result from executing the user_query.
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