import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

connection = None

try:
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "employee_intelligence_system"),
    )

    if connection.is_connected():
        print("Database Connected Successfully")

except mysql.connector.Error as e:
    print("Database Connection Error:", e)