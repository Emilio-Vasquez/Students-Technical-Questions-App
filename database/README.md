# Database Setup

This folder contains the SQL schema for the `technical_questions_app` project. It defines all necessary tables and relationships used across the application, including users, feedback, questions, and submissions.

## File

- `schema.sql`: Contains all SQL commands to initialize the database structure.

## How to Set Up the Database

### 1. Create the database manually

If you're not using the `CREATE DATABASE` command inside `schema.sql`, you can create it manually:

```sql
CREATE DATABASE technical_questions_app;
USE technical_questions_app;
```

### 2. Run the schema script

Use the MySQL CLI to run the script:

```bash
mysql -u your_username -p technical_questions_app < schema.sql
```

Or import the file using a GUI tool like MySQL Workbench, DBeaver, or phpMyAdmin.

---

**Note:** This project does not currently include a `seed.sql` for test data. The database will start empty after running the schema.