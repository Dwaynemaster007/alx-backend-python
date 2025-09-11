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

    def transactional(func):
        """Decorator to manage database transactions."""
        @functools.wraps(func)
        def wrapper(conn, *args, **kwargs):
            try:
                result = func(conn, *args, **kwargs)
                conn.commit()
                print("Transaction committed.")
                return result
            except Exception as e:
                conn.rollback()
                print(f"Transaction rolled back due to error: {e}")
                raise  # Re-raise the exception
        return wrapper

    @with_db_connection 
    @transactional 
    def update_user_email(conn, user_id, new_email): 
        cursor = conn.cursor() 
        cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
        print(f"User {user_id} email updated.")

    # Assuming a users table with a user of id=1
    # Example to test:
    # 1. Update successfully
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    # 2. Test rollback (e.g., passing invalid arguments)
    # update_user_email(user_id='invalid', new_email='test@example.com')
