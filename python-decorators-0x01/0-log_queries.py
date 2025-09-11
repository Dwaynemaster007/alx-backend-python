    import sqlite3
    import functools

    def log_queries(func):
        """Decorator to log SQL queries before execution."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            query = kwargs.get('query')
            if query:
                print(f"Executing query: {query}")
            return func(*args, **kwargs)
        return wrapper

    @log_queries
    def fetch_all_users(query):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results

    # Assuming a users.db file with a 'users' table exists.
    # To test, create a file named users.db and run:
    # conn = sqlite3.connect('users.db')
    # cursor = conn.cursor()
    # cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    # conn.commit()
    # conn.close()
    
    users = fetch_all_users(query="SELECT * FROM users")
