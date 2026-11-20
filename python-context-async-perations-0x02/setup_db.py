#!/usr/bin/python3
"""Create task_database.db with a users table for the context manager and async tasks."""
import sqlite3

USERS = [
    (1, 'Alice', 'alice@example.com', 24),
    (2, 'Bob', 'bob@example.com', 31),
    (3, 'Carol', 'carol@example.com', 45),
    (4, 'Dave', 'dave@example.com', 52),
    (5, 'Eve', 'eve@example.com', 19),
]


def setup_database(db_name='task_database.db'):
    with sqlite3.connect(db_name) as conn:
        conn.execute(
            'CREATE TABLE IF NOT EXISTS users ('
            'id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, age INTEGER NOT NULL)'
        )
        conn.executemany('INSERT OR IGNORE INTO users (id, name, email, age) VALUES (?, ?, ?, ?)', USERS)
    print(f"Database '{db_name}' is ready.")


if __name__ == '__main__':
    setup_database()
