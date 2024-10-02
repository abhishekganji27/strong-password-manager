
from mysql.connector import connect, Error
import mysql.connector


def create_db_in_mysql():
    try:
        with connect(
            host="localhost",
            user="root",
            password="root",
        ) as connection:
            database_name = input("Enter Database Name: ")
            create_db_query = "CREATE DATABASE " + database_name
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
                connection.commit()
            
            show_db_query = "SHOW DATABASES"
            with connection.cursor() as cursor:
                cursor.execute(show_db_query)
                if(cursor.with_rows):
                    res = cursor.fetchall()
                    for row in res:
                        print(row)
                    print(f"\nNo. of rows for '{show_db_query}' query: {len(res)}\n")
                else: 
                    print(f"\nNo rows for '{show_db_query}' query...\n")
            
    except Error as e:
        print(e)

