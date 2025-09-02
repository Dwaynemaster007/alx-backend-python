#!/usr/bin/python3
"""
A script to demonstrate memory-efficient aggregation using a generator.
"""
import mysql.connector
from seed import connect_to_prodev
import sys

def stream_user_ages():
    """
    A generator that streams user ages from the database one by one.

    Yields:
        int: The age of a user.
    """
    connection = None
    try:
        connection = connect_to_prodev()
        if not connection:
            print("Failed to connect to the database.", file=sys.stderr)
            return

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data")

        for row in cursor:
            yield row['age']

    except mysql.connector.Error as err:
        print(f"Database error: {err}", file=sys.stderr)
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection:
            connection.close()

def calculate_average_age():
    """
    Calculates the average age of users without loading all data into memory.
    """
    total_age = 0
    count = 0
    
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age}")
    else:
        print("No users found.")

if __name__ == '__main__':
    calculate_average_age()
