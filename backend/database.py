import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@2004",
    database="employee_intelligence_system"
)

cursor = connection.cursor()

print("Database Connected Successfully")