import tempfile, subprocess, os
import time
import json
import textwrap

def evaluate_python(user_code, test_cases, function_signature):
    """
    Evaluates Python code by injecting test cases and capturing output for each case.
    Uses the full function_signature string (e.g., 'def two_sum(nums, target):')
    Automatically wraps the user code inside the function definition.
    """

    all_results = []
    clean_signature = function_signature.split('#')[0].strip()
    function_name = clean_signature.split('(')[0].replace('def ', '').strip()

    # Ensure function_signature ends with a single colon and no extra spaces
    normalized_signature = function_signature.strip()
    if not normalized_signature.endswith(":"):
        normalized_signature += ":"

    for idx, case in enumerate(test_cases):
        test_input = json.dumps(case["input"])
        expected_output = case["expected_output"]
        description = case.get("description", f"Test Case {idx+1}")

        test_code = f"""
import json
from student_code import *

inputs = json.loads('''{test_input}''')
result = {function_name}(**inputs)
print(json.dumps(result))
"""

        with tempfile.TemporaryDirectory() as tmp_dir:
            code_path = os.path.join(tmp_dir, "student_code.py")
            test_path = os.path.join(tmp_dir, "run_test.py")

            # Sanitize user_code in case they included their own full function definition
            user_lines = user_code.strip().splitlines()
            if user_lines and user_lines[0].strip().startswith("def"):
                # Remove first line (their function definition)
                user_code = "\n".join(user_lines[1:])
                user_code = textwrap.dedent(user_code) 

            # Now wrap their code inside your provided function_signature
            with open(code_path, "w") as f:
                f.write(f"{normalized_signature}\n")
                indented_body = textwrap.indent(user_code.strip(), "    ")
                f.write(indented_body + "\n")

            # Write test runner
            with open(test_path, "w") as f:
                f.write(test_code)

            try:
                start_time = time.perf_counter()
                result = subprocess.run(
                    [
                        "docker", "run", "--rm",
                        "-v", f"{tmp_dir}:/home/student",
                        "safe-python-grader",
                        "python3", "/home/student/run_test.py"
                    ],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                end_time = time.perf_counter()
                elapsed_time = round((end_time - start_time) * 1000, 2)

                output = result.stdout.strip()
                errors = result.stderr.strip()

                try:
                    parsed_output = json.loads(output)
                except Exception:
                    parsed_output = output

                passed = (parsed_output == expected_output) and not errors

                all_results.append({
                    "description": description,
                    "input": case["input"],
                    "expected": expected_output,
                    "result": parsed_output,
                    "passed": passed,
                    "error": errors,
                    "time": f"{elapsed_time} ms"
                })

            except subprocess.TimeoutExpired:
                all_results.append({
                    "description": description,
                    "input": case["input"],
                    "expected": expected_output,
                    "result": None,
                    "passed": False,
                    "error": "Execution timed out.",
                    "time": ">5 sec"
                })

    return all_results