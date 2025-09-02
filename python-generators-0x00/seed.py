#!/usr/bin/python3
"""
A script to set up a MySQL database, create a table, and insert data from a CSV file.
"""
import mysql.connector
import uuid
import csv
import os

# Database configuration
DB_HOST = "localhost"
DB_USER = "dwaynemaster"
DB_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD", "")
DB_NAME = "ALX_prodev"

def connect_db():
    """Connects to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    """Creates the ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database {DB_NAME} created successfully or already exists")
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database {DB_NAME}: {err}")
        return None

def create_table(connection):
    """Creates the user_data table with required fields."""
    cursor = connection.cursor()
    table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5, 0) NOT NULL
    );
    """
    try:
        cursor.execute(table_query)
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Failed to create table: {err}")
    finally:
        cursor.close()

def insert_data(connection, csv_file_path):
    """Inserts data from a CSV file into the user_data table."""
    cursor = connection.cursor()
    
    # Check if the table is empty to avoid duplicate data
    cursor.execute("SELECT COUNT(*) FROM user_data")
    count = cursor.fetchone()[0]
    if count > 0:
        print("Data already exists in user_data. Skipping insertion.")
        cursor.close()
        return

    insert_query = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
    
    try:
        with open(csv_file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader) # Skip the header row
            for row in reader:
                # Assuming the first column of your CSV is the UUID
                row_data = (row[0], row[1], row[2], row[3])
                cursor.execute(insert_query, row_data)
        connection.commit()
        print(f"Data from {csv_file_path} inserted successfully.")
    except FileNotFoundError:
        print(f"Error: The file {csv_file_path} was not found.")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
        connection.rollback()
    finally:
        cursor.close()

if __name__ == '__main__':
    # This block is for testing the functions directly
    print("Testing database connection and setup...")
    conn = connect_db()
    if conn:
        print("Connection to MySQL server successful.")
        create_database(conn)
        conn.close()

        conn_prodev = connect_to_prodev()
        if conn_prodev:
            print("Connection to ALX_prodev database successful.")
            create_table(conn_prodev)
            
            # This part requires 'user_data.csv' to be present
            # For this task, you'll need to manually get the CSV from the Figma link
            csv_path = 'user_data.csv'
            insert_data(conn_prodev, csv_path)
            
            conn_prodev.close()
            print("Connection closed.")
