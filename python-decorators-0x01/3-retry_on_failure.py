import time
    import sqlite3 
    import functools

    def with_db_connection(func):
        """Decorator to handle database connections."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            conn = sqlite3.connect('users.db')
            try:
                result = func(conn, *args, **kwargs)
                return result
            finally:
                conn.close()
        return wrapper

    def retry_on_failure(retries=3, delay=2):
        """Decorator to retry a function on failure."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for i in range(retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        print(f"Attempt {i + 1} failed: {e}")
                        if i < retries - 1:
                            print(f"Retrying in {delay} seconds...")
                            time.sleep(delay)
                        else:
                            print("All retries failed.")
                            raise
            return wrapper
        return decorator

    @with_db_connection
    @retry_on_failure(retries=3, delay=1)
    def fetch_users_with_retry(conn):
        cursor = conn.cursor()
        # Simulate a transient error for testing
        if not hasattr(fetch_users_with_retry, 'attempt'):
            fetch_users_with_retry.attempt = 0
        fetch_users_with_retry.attempt += 1
        if fetch_users_with_retry.attempt < 3:
            raise sqlite3.OperationalError("Database is locked")
        
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

    users = fetch_users_with_retry()
    print(users)
