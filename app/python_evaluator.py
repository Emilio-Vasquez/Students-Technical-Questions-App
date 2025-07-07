import tempfile, subprocess, os  ## we want to make a temporary file and put what the student wrote in there

def evaluate_python(user_code, expected_output):
    import tempfile, subprocess, os

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

        # evaluation
        if errors:
            evaluation = f"❌ Error: {errors}"
        elif output == expected_output:
            evaluation = "✅ Pass!"
        else:
            evaluation = f"❌ Fail: Output does not match expected."

        MAX_OUTPUT_LINES = 20

        if output:
            output_lines = output.splitlines()
            if len(output_lines) > MAX_OUTPUT_LINES:
                displayed_output = "\n".join(output_lines[:MAX_OUTPUT_LINES]) + "\n...(truncated)..."
            else:
                displayed_output = output
        else:
            displayed_output = "(no output)"

        # return BOTH evaluation + user output
        return evaluation, displayed_output
    
    except subprocess.TimeoutExpired:
        os.remove(tmp_path)
        return "❌ Fail: Code timed out.", "(no output)"
