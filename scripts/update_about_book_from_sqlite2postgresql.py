import sqlite3
import psycopg2
from psycopg2 import Error

about_records = []

# export data from sqlite
try:
    sqliteConnection = sqlite3.connect('../db.sqlite3')
    cursor = sqliteConnection.cursor()
    print("Database created and Successfully Connected to SQLite")

    cursor.execute('SELECT * FROM scripture_book')
    records = cursor.fetchall()

    about_records = [(record[0] ,record[7]) for record in records]
    print(about_records)

    cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")


# Import the exported data into postgresql db
try:
    # Connect to an existing database
    connection = psycopg2.connect(user="emadba",
                                  password="emaddbapwd4POST",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="churchtmp")

    connection.autocommit = True

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")

    
    # Executing a SQL query
    for id, value in about_records:
        # cursor.execute(f"INSERT INTO book_about_tmp(content) VALUES ('{record}')")
        cursor.execute(f"UPDATE book_about_tmp SET book_about = '{value}' WHERE id={id}")
        print(id, value)
    
    cursor.execute('SELECT * FROM book_about_tmp')
    cursor.execute("SELECT version();")
    # Fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

