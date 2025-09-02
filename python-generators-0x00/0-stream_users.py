#!/usr/bin/python3
"""
A generator function that streams rows from a MySQL database one by one.
"""
import mysql.connector
from seed import connect_to_prodev
import os

def stream_users():
    """
    Streams rows from the user_data table using a generator.
    
    Yields:
        dict: A dictionary representing a single user record.
    """
    connection = None
    try:
        connection = connect_to_prodev()
        if not connection:
            print("Failed to connect to the database.")
            return

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
            
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    # This block is for testing purposes only, if you need to run this file directly
    print("Streaming users from the database...")
    from itertools import islice
    for user in islice(stream_users(), 6):
        print(user)
