"""
User-submitted solution script for code evaluation.

This file is dynamically executed by the evaluator to test user implementations.
Check the python and sql evaluators for this, and the questions.py script.
"""

def solution(s):
    """
    Determines whether the input string is a palindrome, considering only alphanumeric characters and ignoring case.

    Parameters:
        s (str): The input string to evaluate.

    Returns:
        bool: True if the cleaned string is a palindrome, False otherwise.
    """
    cleaned = ''

    for char in s:

        if char.isalnum():

            cleaned += char.lower()

    return cleaned == cleaned[::-1]