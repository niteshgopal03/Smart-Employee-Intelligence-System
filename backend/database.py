import mysql.connector

try:

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@2004",
        database="employee_intelligence_system"
    )

    if connection.is_connected():

        print("Database Connected Successfully")

except mysql.connector.Error as e:

    print("Database Connection Error :", e)