from app.questions import evaluate_submission ## importing the evaluate_submission function

def test_python():
    code = """
nums = [2,7,11,15]
target = 9
for i in range(len(nums)):
    for j in range(i+1, len(nums)):
        if nums[i] + nums[j] == target:
            print([i, j])
"""
    expected = "[0, 1]"
    print(evaluate_submission(code, expected, language="python")) ## the function expects the user's code, expected result, and the language

## Let's make this file be able to be runnable by itself.
if __name__ == "__main__":
    test_python()

## Tested with code: python -m app.test.test_python_evaluator, on the Technical-Questions-App directory