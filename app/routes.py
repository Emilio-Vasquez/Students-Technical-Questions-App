from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from .questions import load_questions, evaluate_submission ## importing the evaluate_submission function, this will load the questions up for us (function)
from .register import handle_registration ## This imports the function that handles the registration steps
from .user_validators import is_username_available, is_email_available ## these are the functions that we use to see if email and usernames are valid
from .login import handle_login ## This is the function that handles the login to check if the username and password match
from .feedback import handle_feedback ## This is the function the handles the feedback logic
from .account_settings import handle_account_settings ## Need this to handle the get,post information to change account settings
from .question_aggregates import get_question_counts ## Need this to get the aggregated counts of the questions
from .user_submissions import store_user_submission ## store_user_submission function has the logic to store user submissions
from .db import get_db_connection ## getting the database connection
from .sql_table_metadata import extract_sql_metadata ## This gets the sql metadata to give to the user for a nice table display on their questions

main = Blueprint('main', __name__)

@main.route('/')
def home():
    counts = get_question_counts()
    return render_template('home.html', counts = counts)

@main.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        ## login.py script called here
        success, message = handle_login(request.form)
        if success:
            flash("Login Successful!", "success")
            return redirect(url_for('main.home'))
        else:
            flash(message, "danger")
            return render_template('login.html')
    return render_template('login.html')

@main.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        ## register.py script called here, we can call the handle_registration function for that
        success, message = handle_registration(request.form)
        if success:
            flash(message, "success")
            return redirect(url_for("main.login")) ## If registration successful bring user to the login page
        else:
            flash(message, "danger")
            return redirect(url_for("main.register")) ## if not, then bro gotta try again
    return render_template('register.html')

## This is an add on to the registeration, checking if the usernames are valid and emails are valid (if they're not already in db):
@main.route('/check_username', methods=['POST'])
def check_username():
    data = request.get_json()
    username = data.get('username', '').strip()
    available, message = is_username_available(username)
    return {'available': available, 'message': message}

@main.route('/check_email', methods=['POST'])
def check_email():
    data = request.get_json()
    email = data.get('email', '').strip()
    available, message = is_email_available(email)
    return {'available': available, 'message': message}

@main.route('/feedback', methods = ['GET','POST'])
def feedback():
    if request.method == 'POST':
        success, message = handle_feedback(request.form, session)
        if success:
            flash(message, "success")
            return redirect(url_for('main.feedback'))
        else:
            flash(message, "danger")

    return render_template('feedback.html')

@main.route('/questions', methods = ['GET','POST'])
def questions():
    ## WE IMPORTED 'load_questions' variable at the top from the questions.py file
    questions = load_questions() ## this holds a function that opens the json file that has all the questions
    ## Now this 'questions' variable holds the list of questions that will be displayed in the html page
    ## We will send this by saying, once we render_template, the data we pass through it will be the 'questions' variable.
    ## This is second argument: questions = questions, that's how the data gets passed to the HTML
    return render_template('questions.html', questions = questions)

@main.route('/question_detail/<string:slug>', methods = ['GET','POST']) ## slug is the question title, but in a route friendly syntax
def question_detail(slug): ## The question.title will be obtained when the user clicks the question from the questions.html page
    questions = load_questions() ## getting the questions from the questions.py, which loads a function to open and read the json file with the data
    question = next((q for q in questions if q['slug'] == slug), None)

    if not question:
        flash("Question is not found", "danger")
        return redirect(url_for('main.questions'))
    
    previous_answer = None
    previous_language = question["language"]  # fallback default

    if 'username' in session:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT us.code_submission, us.language
                FROM user_submissions us
                JOIN users u ON u.id = us.user_id
                WHERE us.question_slug=%s AND LOWER(u.username) = LOWER(%s)
            """, (slug, session['username']))
            row = cursor.fetchone()
            if row:
                previous_answer = row["code_submission"]
                previous_language = row["language"]
        conn.close()

    answer = ""
    submitted_answer = previous_answer  # prepopulate with their latest
    evaluation = None
    user_output = None

    if question["language"] == "sql" and question.get("setup_sql"):
        table_metadata = extract_sql_metadata(question["setup_sql"])
    else:
        table_metadata = None

    if request.method == 'POST':
        answer = request.form.get("answer")
        language = request.form.get("language")

        if language not in ["python", "sql"]:
            flash("Invalid language selection", "danger")
            return redirect(url_for("main.question_detail", slug=slug))

        # your evaluation function
        evaluation, user_output = evaluate_submission(
            answer,
            question.get("expected_output"),
            language,
            question.get("setup_sql")
        )

        if 'username' in session:
            passed = evaluation.startswith("✅")
            store_user_submission(
                username=session['username'],
                slug=slug,
                answer=answer,
                language=language,
                passed=passed
            )

        # we want to show these on the page
        submitted_answer = answer
        previous_language = language ## Take this immediately so that it doesnt switch back to default language when you submit code for evaluation
        ## duplicate call: evaluation, user_output = evaluate_submission(answer, question.get("expected_output"), language)  # if you want to display “their code” as “their output”
        # you could swap in real execution output if you have it

    return render_template(
        "question_detail.html",
        question=question,
        evaluation=evaluation,
        submitted_answer=submitted_answer if submitted_answer else "",  # safely default to blank
        user_output=user_output,
        previous_language=previous_language,
        table_metadata=table_metadata
    )

@main.route('/logout') ## Flask automatically uses GET method if you don't specify, so when the user clciks the button it redirects
def logout():
    session.pop('username', None)
    flash("You have been logged out!", "info")
    return redirect(url_for('main.home'))

@main.route('/account_settings', methods=['GET','POST']) ## Flask automatically uses GET method if you don't specify, so when the user clciks the button it redirects
def account_settings():
    return handle_account_settings()