from app.questions import evaluate_submission

def test_sql():
    sql = "SELECT SUM(amount) FROM sales;"
    expected = "1000"
    print(evaluate_submission(sql, expected, language="sql"))

if __name__ == "__main__":
    test_sql()

## Tested with code: python -m app.test.test_sql_evaluator, on the Technical-Questions-App directory