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
    with open(file_path, 'r') as f:
        return json.load(f) ## this is to open and read the files

def evaluate_submission(user_code, expected_output, language="python"):
    """
    Just finished the Dockerfile and tested it, should be fine now

    Dispatches student code to the appropriate grader:
    - Python code runs in a Docker sandbox
    - SQL code runs in a local SQLite in-memory test
    """
    if language == "python":
        return evaluate_python(user_code, expected_output)
    elif language == "sql":
        return evaluate_sql(user_code, expected_output)
    else:
        return "Unknown language. Cannot evaluate."