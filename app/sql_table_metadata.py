"""
Utilities for extracting table metadata and sample rows from SQL setup scripts.

This module uses an in-memory SQLite database to parse a provided SQL string
and return schema information and sample data for each table.
"""
import sqlite3

def extract_sql_metadata(setup_sql):
    """
    Parses setup SQL and returns metadata for all created tables.

    This function executes the provided SQL (e.g., CREATE TABLE and INSERT statements)
    in a temporary in-memory SQLite database. It then extracts:
    - Table names
    - Column names and data types
    - The first 5 rows of data for each table

    Args:
        setup_sql (str or list): SQL script(s) to execute, either as a string
                                 or a list of SQL lines.

    Returns:
        list: A list of dictionaries containing:
              - table_name (str)
              - columns (list of {"name": str, "type": str})
              - rows (list of tuples)
              If an error occurs, returns a list with a single dictionary
              containing an "error" key.
    """
    # Normalize setup_sql to a string
    if isinstance(setup_sql, list):
        setup_sql = "\n".join(setup_sql)
    elif not isinstance(setup_sql, str):
        setup_sql = ""

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    metadata = []

    try:
        cursor.executescript(setup_sql)

        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]

        for table in tables:
            # Get column info
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()

            # Get first 5 rows
            cursor.execute(f"SELECT * FROM {table} LIMIT 5;")
            rows = cursor.fetchall()

            metadata.append({
                "table_name": table,
                "columns": [{"name": col[1], "type": col[2]} for col in columns],
                "rows": rows
            })

        return metadata

    except sqlite3.Error as e:
        return [{"error": f"SQL error: {e}"}]

    finally:
        conn.close()
