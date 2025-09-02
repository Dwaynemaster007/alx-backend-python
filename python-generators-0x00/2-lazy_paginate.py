#!/usr/bin/python3
"""
A script to demonstrate lazy loading of paginated data using a generator.
"""
import mysql.connector
from seed import connect_to_prodev

def paginate_users(page_size, offset):
    """
    Fetches a single page of user data from the database.

    Args:
        page_size (int): The number of users to fetch per page.
        offset (int): The starting position for the data retrieval.

    Returns:
        list: A list of dictionaries, where each dictionary represents a user record.
    """
    connection = None
    rows = []
    try:
        connection = connect_to_prodev()
        if not connection:
            print("Failed to connect to the database.")
            return rows

        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection:
            connection.close()
            
    return rows

def lazy_paginate(page_size):
    """
    A generator that lazily fetches and yields pages of user data.

    Args:
        page_size (int): The number of users to fetch per page.
    
    Yields:
        list: A list of dictionaries, representing a page of user records.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

if __name__ == '__main__':
    # This block is for testing purposes, mirroring the provided main script
    import sys
    
    try:
        for page in lazy_paginate(100):
            for user in page:
                print(user)

    except BrokenPipeError:
        sys.stderr.close()
