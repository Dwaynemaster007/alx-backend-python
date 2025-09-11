# python-decorators-0x01

This project explores the power of Python decorators by implementing them to solve common challenges in database management. The goal is to create reusable, clean, and robust code for tasks like logging queries, managing connections, handling transactions, retrying failures, and caching results.

## Learning Objectives

By completing this project, I have gained a deeper understanding of:
* **Python Decorators:** How to create and use them to wrap functions.
* **Database Management:** Automating repetitive tasks like connection handling and transaction management.
* **Resilience and Performance:** Implementing retry mechanisms for transient errors and caching to optimize query performance.

## Project Files

* `0-log_queries.py`: A decorator that logs SQL queries before execution.
* `1-with_db_connection.py`: A decorator that automatically handles opening and closing a database connection for a function.
* `2-transactional.py`: A decorator that ensures database operations are atomic, either committing all changes on success or rolling back on failure.
* `3-retry_on_failure.py`: A decorator that retries a function a specified number of times if it encounters an exception.
* `4-cache_query.py`: A decorator that caches the results of a database query to prevent redundant calls.

## Prerequisites

* Python 3.8+
* SQLite3 database with a `users` table for testing.
* Basic understanding of Python and SQL.

## How to Run

To run any of the scripts, navigate to the `python-decorators-0x01` directory and execute the file using `python3`.

**Example:**
```bash
python3 0-log_queries.py
