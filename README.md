# Technical Questions App

## Overview

**Technical Questions App** is an interactive coding practice platform built for students at **Union College of Union County, NJ (UCNJ)**. Designed to simulate real-world technical interviews, it helps students sharpen their skills in **Python** and **SQL** through hands-on problem solving.

Students can register, log in, browse categorized questions, write and submit code directly in the browser, and receive instant feedback. The platform features built-in progress tracking and secure sandboxed code evaluation—all wrapped in a responsive, user-friendly interface.

## Purpose

This project was created to:

- Help UCNJ students practice for coding interviews at their own pace.
- Build fluency in Python and SQL through real-world challenges.
- Track individual student progress across categories.
- Introduce students to a modern, browser-based coding workflow.

## Project Structure

```
Technical-Questions-App/
├── app/
│   ├── __init__.py
│   ├── account_settings.py
│   ├── comments.py
│   ├── db.py
│   ├── feedback.py
│   ├── forgot_password.py
│   ├── login.py
│   ├── mailer.py
│   ├── python_evaluator.py
│   ├── question_aggregates.py
│   ├── questions.py
│   ├── register.py
│   ├── reset_password.py
│   ├── routes.py
│   ├── sql_evaluator.py
│   ├── sql_table_metadata.py
│   ├── user_submissions.py
│   ├── user_validators.py
│   ├── admin/
│   │   ├── __init__.py
│   │   ├── dashboard.py
│   │   ├── feedback.py
│   │   ├── questions.py
│   │   ├── routes.py
│   │   ├── submissions.py
│   │   ├── test_cases.py
│   │   ├── tools.py
│   │   ├── users.py
│   │   └── utils.py
│   ├── data/
│   │   ├── answer_key.json
│   │   └── questions.json
│   ├── grader/
│   │   └── Dockerfile
│   ├── scripts/
│   │   ├── migrate_questions.py
│   │   └── migrate_test_cases.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── admin.css
│   │   │   ├── certifications.css
│   │   │   ├── events.css
│   │   │   └── ucnj_style.css
│   │   ├── images/
│   │   │   ├── emilio.PNG
│   │   │   ├── linux-intro.jpg
│   │   │   ├── scavenger-hunt.svg
│   │   │   ├── thumbs-up.svg
│   │   │   ├── visualization-jam.jpg
│   │   │   └── favicon.ico
│   │   ├── js/
│   │   │   ├── account_settings.js
│   │   │   ├── add_question.js
│   │   │   ├── code_editor.js
│   │   │   ├── comment_voting.js
│   │   │   ├── comments.js
│   │   │   ├── flash.js
│   │   │   ├── handle_not_logged.js
│   │   │   ├── login.js
│   │   │   ├── question_filter.js
│   │   │   ├── question_sort.js
│   │   │   ├── register.js
│   │   │   ├── reset_password.js
│   │   │   └── test_cases.js
│   ├── templates/
│   │   ├── admin/
│   │   │   ├── add_question.html
│   │   │   ├── dashboard.html
│   │   │   ├── edit_question_list.html
│   │   │   ├── edit_question.html
│   │   │   └── manage_test_cases.html
│   │   ├── account_settings.html
│   │   ├── base.html
│   │   ├── certifications.html
│   │   ├── events.html
│   │   ├── feedback.html
│   │   ├── forgot_password.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── question_detail.html
│   │   ├── questions.html
│   │   ├── register.html
│   │   └── reset_password.html
│   ├── test/
│   │   ├── test_email_sender.py
│   │   ├── test_mysql_connection.py
│   │   ├── test_python_evaluator.py
│   │   └── test_sql_evaluator.py
├── database/
│   ├── schema.sql
│   └── README.md
├── .env
├── .gitignore
├── config.py
├── LICENSE
├── README.md
├── run.py
└── student_code.py
```

## Key Features

### 1. User Authentication

Users can create accounts with a username, email, and password.  
Passwords are securely hashed using bcrypt.  
Session management is handled through Flask's built-in session system.

### 2. Question Management

Questions are stored in a MySQL database and organized into three categories: Computer Science, Data Science, and Databases.  
Each question includes a title, slug, category, language, prompt, and a set of test cases for evaluation.

### 3. Code Evaluation

Python code is executed in a secure, sandboxed environment using Docker to prevent unsafe behavior.  
SQL submissions are executed against an in-memory test database and evaluated based on expected output.

### 4. Language Toggle with Persistence

Each question supports both Python and SQL implementations.  
Users can switch between the two languages, and their selection is retained across reloads and submissions.

### 5. Theme Switching

The interface supports both light and dark themes.  
The selected theme is saved using localStorage and applied consistently across sessions.
However, this light/dark theme is not applied to the whole page, only the textarea for coding.

### 6. Progress Tracking

Users can monitor their progress within each category.  
Both the total number of questions and the number completed are displayed using visual progress indicators.

### 7. Account Settings

Users can manage their account through the settings page.  
They can change their password, update their phone number, and verify their email address.  
Progress data is displayed using a card-based layout for clarity.

### 8. Question Submission and Feedback

Users can submit solutions to each question and immediately view evaluation results.  
A dedicated feedback page is available for users to submit comments or suggestions about the platform.

## Docker Integration

Python code is executed in an isolated Docker container to ensure security.  
The grader container runs the user’s code separately and returns the result to the main Flask application.  
This architecture prevents malicious or unstable code from affecting the host system.

## Database Migration

Initial question data is defined in a JSON file located at `app/data/questions.json`.  
This data is imported into the MySQL `questions` table using the migration script `app/scripts/migrate_questions.py`.
The data for the test cases are also within the keys of the `questions.json` file, but the table filled is
`question_test_cases`, and the migration script is `app/scripts/migrate_test_cases.py`.

## Testing

Unit tests are located in the `app/test/` directory.  
They cover the following functionality:

- Python code evaluation
- SQL query evaluation
- Database connection handling

## Technologies Used

- Flask for backend routing, templating, and session control  
- MySQL for relational data storage  
- Docker for secure, sandboxed code execution  
- JavaScript for client-side interactivity  
- HTML and CSS (UCNJ design theme) for layout and responsiveness  
- bcrypt for password encryption and verification

## Running the App

### Prerequisites

- Python 3.9 or higher  
- Docker installed and running  
- MySQL server with appropriate user credentials

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Technical-Questions-App
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Setup `.env` file with database credentials and secrets.
4. Run the migration script:
   ```bash
   python -m app.scripts.migrate_questions
   python -m app.scripts.migrate_test_cases
   ```
   > Note: The question data must be provided by you. The app expects a file named questions.json located in the app/data/ directory.
   > You must create this file yourself or acquire it from a source you trust.
   The file should follow this structure for Python questions:
   ```json
   [
        {
            "id": 1,
            "title": "",
            "slug": "",
            "prompt": "",
            "language": "python",
            "category": "Computer Science",
            "difficulty": "",
            "function_signature": "def solution(nums, target):",
            "test_cases": [
            {
                "input": "",
                "expected_output": "",
                "description": ""
            }
            ]
        }
    ]
   ```

   For SQL questions, replace the `language`, `function_signature`, and ``test_cases` accordingly:
   ```json
   {
        "language": "sql",
        "test_cases": [
            {
            "description": "Find empty neighborhoods",
            "setup_sql": "CREATE TABLE users (id INT, neighborhood VARCHAR(100)); INSERT INTO users VALUES (1, 'Downtown');",
            "expected_output": []
            }
        ]
    }
    ```

5. Start the app:
   ```bash
   python run.py
   ```

## Contribution Guidelines

- Organize code into clean, modular components.
- Include meaningful docstrings and inline comments for maintainability.
- Use tools like `black` or `flake8` to ensure code is consistently formatted.
- When editing UI elements, follow the design patterns defined in `static/css/ucnj_style.css`.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).  
You are free to use, modify, and distribute this software, provided that the original license and copyright notice are included.

