import sqlite3 
    import functools

    def with_db_connection(func):
        """Decorator to handle database connections."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            conn = sqlite3.connect('users.db')
            try:
                # Pass the connection object as the first argument
                result = func(conn, *args, **kwargs)
                return result
            finally:
                conn.close()
        return wrapper

    @with_db_connection 
    def get_user_by_id(conn, user_id): 
        cursor = conn.cursor() 
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
        return cursor.fetchone() 

    # Assuming a users.db with a users table and at least one user exists
    user = get_user_by_id(user_id=1)
    print(user)
