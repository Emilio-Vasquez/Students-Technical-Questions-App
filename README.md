# Technical Questions App

## Overview

The Technical Questions App is a web-based learning platform developed to support students at Union College of Union County, NJ (UCNJ) in preparing for technical interviews and strengthening their coding and data-related skills. It serves as a practice hub for students studying Computer Science, Data Science, and Databases.

This platform features an interactive interface where users can register, log in, attempt questions, submit answers, and track their progress. It supports both Python and SQL questions and includes an integrated code evaluator for each. The entire system emphasizes user experience and secure, isolated code execution.

## Purpose

The main goal of this project is to:

- Provide UCNJ students with a self-paced technical interview practice platform.
- Expose students to real-world coding challenges in Python and SQL.
- Track student progress over time to help identify areas of improvement.
- Familiarize students with a modern web-based interface and responsive features.

## Project Structure

```
Technical-Questions-App/
├── app/
│   ├── __init__.py
│   ├── account_settings.py
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
│   ├── data/
│   │   └── questions.json
│   ├── grader/
│   │   └── Dockerfile
│   ├── scripts/
│   │   ├── migrate_questions.py
│   │   └── migrate_test_cases.py
│   ├── static/
│   │   ├── css/
│   │   │   └── ucnj_style.css
│   │   ├── images/
│   │   │   ├── emilio.PNG
│   │   │   └── favicon.ico
│   │   ├── js/
│   │   │   ├── account_settings.js
│   │   │   ├── code_editor.js
│   │   │   ├── flash.js
│   │   │   ├── login.js
│   │   │   ├── question_filter.js
│   │   │   ├── question_sort.js
│   │   │   ├── register.js
│   │   │   └── reset_password.js
│   ├── templates/
│   │   ├── account_settings.html
│   │   ├── base.html
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
├── database_queries.sql
├── LICENSE
├── README.md
├── run.py
└── student_code.py
```

## Key Features

### 1. User Authentication

- Users can register with a username, email, and password.
- Login system with password hashing via bcrypt.
- Session management using Flask sessions.

### 2. Question Management

- Questions are stored in a MySQL database and categorized as:
  - Computer Science
  - Data Science (a derived aggregate of CS + Databases)
  - Databases
- Each question has metadata such as title, slug, category, language, prompt, and expected output.

### 3. Code Evaluation

- **Python Evaluator:** Uses Docker to run user-submitted Python code in a secure sandbox.
- **SQL Evaluator:** Executes submitted SQL queries against a test database to validate correctness.

### 4. Language Toggle and Persistence

- Users can switch between Python and SQL views per question.
- Selection persists across page reloads and form submissions.

### 5. Theme Switching

- Light and dark mode support with persistent theme selection using localStorage.

### 6. Progress Tracking

- Users can view progress per category.
- Total questions and completed counts are shown using dynamic progress bars.

### 7. Account Settings

- Allows users to:
  - Change their password.
  - Add or update their phone number.
  - (Future Feature) Verify their email address.
- Progress is visually represented in a card layout.

### 8. Question Submission & Feedback

- Users can submit answers and receive instant feedback on correctness.
- Feedback page available for submitting platform-related comments or suggestions.

## Docker Integration

To safely execute potentially untrusted Python code, this project uses Docker to isolate code execution environments. A separate `grader` container runs user code and returns the results back to the main Flask application. This separation ensures system-level security.

## Database Migration

- Initial question data is migrated from `questions.json` in `app/data/` into a MySQL `questions` table using a migration script located in `app/scripts/migrate_questions.py`.

## Testing

Unit tests are stored in the `app/test/` folder and cover:

- Python evaluator functionality
- SQL evaluator functionality
- MySQL database connectivity

## Technologies Used

- **Flask** for backend routing and session management
- **MySQL** for relational data persistence
- **Docker** for code sandboxing
- **JavaScript** for client-side interactivity
- **HTML/CSS (UCNJ styling)** for responsive layout
- **bcrypt** for password hashing

## Running the App

### Prerequisites:

- Python 3.9+
- Docker
- MySQL Server

### Setup

1. Clone the repository:
   ```bash
   git clone <repo-url>
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
   ```
5. Start the app:
   ```bash
   python run.py
   ```

## Contribution Guidelines

- Keep code modular and clean.
- Write docstrings and comments where needed.
- Use `black` or `flake8` to format Python files.
- For UI, keep consistency with existing styles in `static/css/ucnj_style.css`.

## License

This project is internal to UCNJ and not currently open for public distribution.

