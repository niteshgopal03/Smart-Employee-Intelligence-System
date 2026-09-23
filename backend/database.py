import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

connection = None

try:
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "4000")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv(
            "DB_NAME",
            "employee_intelligence_system"
        ),

        # TiDB Cloud TLS
        ssl_ca=os.getenv("DB_SSL_CA"),
        ssl_verify_cert=True,
        ssl_verify_identity=True,
    )

    if connection.is_connected():
        print("TiDB Database Connected Successfully")

except mysql.connector.Error as e:
    print("Database Connection Error:", e)