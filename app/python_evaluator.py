import tempfile, subprocess, os  ## we want to make a temporary file and put what the student wrote in there
import time  # Add this import

def evaluate_python(user_code, expected_output):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
        tmp.write(user_code)
        tmp_path = tmp.name

    try:
        start_time = time.perf_counter()  # Start timer
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                "-v", f"{tmp_path}:/home/student/student_code.py:ro",
                "safe-python-grader",
                "python3", "/home/student/student_code.py"
            ],
            capture_output=True,
            text=True,
            timeout=5
        )
        end_time = time.perf_counter()  # End timer
        elapsed_time = round((end_time - start_time) * 1000, 2)  # changing it into milliseconds

        output = result.stdout.strip()
        errors = result.stderr.strip()
        os.remove(tmp_path)

        if errors:
            evaluation = f"❌ Error: {errors}"
        elif output == expected_output:
            evaluation = "✅ Pass!"
        else:
            evaluation = f"❌ Fail: Output does not match expected."

        MAX_OUTPUT_LINES = 20
        output_lines = output.splitlines() if output else []
        displayed_output = (
            "\n".join(output_lines[:MAX_OUTPUT_LINES]) +
            ("\n...(truncated)..." if len(output_lines) > MAX_OUTPUT_LINES else "")
        ) if output else "(no output)"

        # Add timing to evaluation message
        evaluation += f" (⏱ {elapsed_time} ms)"
        return evaluation, displayed_output

    except subprocess.TimeoutExpired:
        os.remove(tmp_path)
        return "❌ Fail: Code timed out. (⏱ >5 sec)", "(no output)"