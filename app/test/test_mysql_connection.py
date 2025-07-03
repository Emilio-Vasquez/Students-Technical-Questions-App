import pymysql
from dotenv import load_dotenv
import os

## load .env this is where all my keys are in
load_dotenv()

def test_mysql_connection():
    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()
            print(f"Connected to database: {db_name[0]}")
    finally:
        connection.close()

if __name__ == "__main__":
    test_mysql_connection()

## To thest the sql connection: python -m app.test.test_mysql_connection on the root directory Technical-Questions-App