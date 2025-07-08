"""
questions.py

This module handles loading technical questions from a JSON file and evaluating user submissions.
It supports both Python and SQL questions by delegating evaluation logic to language-specific evaluators.

Functions:
- load_questions(): Load all technical questions from the JSON file.
- evaluate_submission(): Evaluate a user's submitted code against a set of test cases.
"""
import json
import os
from .sql_evaluator import evaluate_sql
from .python_evaluator import evaluate_python

def load_questions():
    """
    Load all technical questions from the 'questions.json' file in the data directory.

    Returns:
        list: A list of question dictionaries parsed from the JSON file.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'questions.json') ## this will join the folder's name: 'app/' and connect it with 'data' and 'questions.json
    ## that's app/data/questions.json and that's where the questions are stored in a json file.
    ## in this json file, you will see: "slug", we use "slugs" because they're route friendly, not having uppercase or spaces.
    ## There are no comments allowed in json so we had to remove all comments
    ## JSON also uses double quotes for all keys and strings
    with open('app/data/questions.json', encoding='utf-8') as f:
        return json.load(f) ## this is to open and read the files

def evaluate_submission(user_code, test_cases, language="python", function_signature=None):
    """
    Evaluate user-submitted code against all test cases using the appropriate language evaluator.

    Args:
        user_code (str): The code submitted by the user.
        test_cases (list): A list of test case dictionaries containing 'expected_output', 
                           optional 'setup_sql', and other metadata.
        language (str): The language of the code, either 'python' or 'sql'. Defaults to 'python'.
        function_signature (str, optional): The function signature to prepend for Python evaluations.

    Returns:
        list: A list of result dictionaries for each test case with:
              - description (str)
              - input (any)
              - expected (any)
              - result (any)
              - passed (bool)
              - error (str or None)
              - time (str)
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