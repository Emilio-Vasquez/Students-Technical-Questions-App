import json
import os
from .sql_evaluator import evaluate_sql
from .python_evaluator import evaluate_python

def load_questions():
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'questions.json') ## this will join the folder's name: 'app/' and connect it with 'data' and 'questions.json
    ## that's app/data/questions.json and that's where the questions are stored in a json file.
    ## in this json file, you will see: "slug", we use "slugs" because they're route friendly, not having uppercase or spaces.
    ## There are no comments allowed in json so we had to remove all comments
    ## JSON also uses double quotes for all keys and strings
    with open('app/data/questions.json', encoding='utf-8') as f:
        return json.load(f) ## this is to open and read the files

def evaluate_submission(user_code, test_cases, language="python", function_signature=None):
    """
    Dispatches user code to the appropriate evaluator with all test case metadata.
    Returns full evaluation results for frontend display.
    """
    if language == "python":
        signature = function_signature or "def solution():"
        return evaluate_python(user_code, test_cases, signature)

    elif language == "sql":
        evaluations = []
        for idx, case in enumerate(test_cases):
            result, output = evaluate_sql(
                user_code,
                case["expected_output"],
                case.get("setup_sql")
            )
            evaluations.append({
                "description": case.get("description", f"Test case {idx + 1}"),
                "input": case.get("input", "N/A"),  # SQL might not have this
                "expected": case["expected_output"],
                "result": output,
                "passed": result.startswith("✅"),
                "error": None if result.startswith("✅") else result,
                "time": "N/A"  # You can optionally add timing here
            })
        return evaluations

    else:
        return [{
            "description": "Unknown language",
            "input": None,
            "expected": None,
            "result": None,
            "passed": False,
            "error": "Unsupported language",
            "time": "N/A"
        }]