"""
db.py

Provides a function to establish and return a connection to the MySQL database
using credentials stored in environment variables.
"""
import pymysql
from dotenv import load_dotenv
import os

## loading the .env variables that are secret to initial my db connection
load_dotenv()

def get_db_connection():
    """
    Establishes and returns a new connection to the MySQL database.

    Returns:
        pymysql.connections.Connection: A connection object with DictCursor enabled.

    Environment Variables Used:
        - DB_HOST: Database host
        - DB_USER: Database user
        - DB_PASSWORD: Database password
        - DB_NAME: Name of the database
    """
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )