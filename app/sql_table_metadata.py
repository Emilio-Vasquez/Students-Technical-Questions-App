import sqlite3

def extract_sql_metadata(setup_sql):
    """
    Returns table descriptions and sample data from the setup SQL.
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
