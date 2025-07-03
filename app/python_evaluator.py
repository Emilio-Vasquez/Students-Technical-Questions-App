import tempfile, subprocess, os  ## we want to make a temporary file and put what the student wrote in there

def evaluate_python(user_code, expected_output):

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
        tmp.write(user_code)
        tmp_path = tmp.name

    try:
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
        output = result.stdout.strip()
        errors = result.stderr.strip()
        os.remove(tmp_path)

        if errors:
            return f"Error: {errors}"
        if output == expected_output:
            return "✅ Pass!"
        else:
            return f"❌ Fail. Got: {output}, Expected: {expected_output}"
    except subprocess.TimeoutExpired:
        return "❌ Fail: Code timed out."
