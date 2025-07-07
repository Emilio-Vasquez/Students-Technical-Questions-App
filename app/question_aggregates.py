from .questions import load_questions

def get_question_counts():
    """
    Calculates the number of available questions for each category.

    Returns:
        dict: A dictionary with counts for each category:
              - 'compsci': number of Computer Science questions
              - 'datasci': number of Data Science questions
              - 'databases': number of Databases questions
    """
    questions = load_questions()
    compsci_count = sum(1 for q in questions if q['category'] == 'Computer Science')
    datasci_count = sum(1 for q in questions if q['category'] == 'Data Science')
    databases_count = sum(1 for q in questions if q['category'] == 'Databases')

    return {
        'compsci': compsci_count,
        'datasci': datasci_count,
        'databases': databases_count
    }
