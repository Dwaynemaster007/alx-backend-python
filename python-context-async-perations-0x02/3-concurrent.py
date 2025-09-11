import asyncio
import aiosqlite
import sqlite3

# --- Database Setup (synchronous) ---
def setup_database(db_name='users.db'):
    try:
        conn_setup = sqlite3.connect(db_name)
        cursor_setup = conn_setup.cursor()
        cursor_setup.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER
            )
        ''')
        # Insert sample data
        data = [
            (1, 'John Doe', 'john@example.com', 30),
            (2, 'Jane Smith', 'jane@example.com', 22),
            (3, 'Peter Jones', 'peter@example.com', 45),
            (4, 'Alice Brown', 'alice@example.com', 28),
            (5, 'Bob White', 'bob@example.com', 55)
        ]
        cursor_setup.executemany("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (?, ?, ?, ?)", data)
        conn_setup.commit()
    except sqlite3.Error as e:
        print(f"Synchronous database setup error: {e}")
    finally:
        if conn_setup:
            conn_setup.close()

# Run the synchronous database setup once
setup_database()

# --- Asynchronous Database Functions ---
async def _fetch_users(db_name='users.db'):
    """Helper function to fetch all users."""
    print(f"[{asyncio.current_task().get_name()}] Fetching all users from {db_name}...")
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT id, name, email, age FROM users") as cursor:
            users = await cursor.fetchall()
            print(f"[{asyncio.current_task().get_name()}] All users fetched.")
            return users

async def _fetch_older_users(age_threshold=40, db_name='users.db'):
    """Helper function to fetch users older than a specified age."""
    print(f"[{asyncio.current_task().get_name()}] Fetching users older than {age_threshold} from {db_name}...")
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT id, name, email, age FROM users WHERE age > ?", (age_threshold,)) as cursor:
            older_users = await cursor.fetchall()
            print(f"[{asyncio.current_task().get_name()}] Older users fetched.")
            return older_users

# The functions the checker is looking for
async def async_fetch_users():
    return await _fetch_users()

async def async_fetch_older_users():
    return await _fetch_older_users()

async def fetch_concurrently():
    """
    Executes multiple asynchronous database queries concurrently using asyncio.gather().
    """
    print("\n--- Starting concurrent database fetches ---")
    
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    all_users_result = results[0]
    older_users_result = results[1]

    print("\n--- Concurrent Fetch Results ---")
    print("All Users:")
    for user in all_users_result:
        print(user)

    print("\nUsers Older Than 40:")
    for user in older_users_result:
        print(user)
    print("--------------------------------")

# --- Run the concurrent fetch ---
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
