#!/usr/bin/python3
"""
A script to demonstrate batch processing of a large database using generators.
"""
import mysql.connector
from seed import connect_to_prodev
import sys

def stream_users_in_batches(batch_size):
    """
    Streams rows from the user_data table in batches.

    Args:
        batch_size (int): The number of rows to fetch in each batch.

    Yields:
        list: A list of dictionaries, where each dictionary represents a user record.
    """
    connection = None
    try:
        connection = connect_to_prodev()
        if not connection:
            print("Failed to connect to the database.", file=sys.stderr)
            return

        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        while True:
            rows = cursor.fetchmany(size=batch_size)
            if not rows:
                break
            yield rows

    except mysql.connector.Error as err:
        print(f"Database error: {err}", file=sys.stderr)
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection:
            connection.close()

def batch_processing(batch_size):
    """
    Processes each batch of users and filters for users over the age of 25.

    Args:
        batch_size (int): The size of each batch to process.
    
    Yields:
        dict: A dictionary of a user record filtered by age.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user.get('age', 0) > 25:
                yield user

if __name__ == '__main__':
    # Example usage for testing purposes
    print("Streaming and processing users in batches...")
    for user in batch_processing(50):
        print(user)
