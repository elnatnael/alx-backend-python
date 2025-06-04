import time
import mysql.connector
import functools

# ✅ DB Connection Decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='messimera12',
            database='alx_prodev'
        )
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# ✅ Retry Decorator
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"[RETRY] Attempt {attempts} failed: {e}")
                    if attempts < retries:
                        time.sleep(delay)
                    else:
                        print("[ERROR] Max retries reached.")
                        raise
        return wrapper
    return decorator

# ✅ Function to fetch users with retry logic
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")
    return cursor.fetchall()

# ✅ Test call
users = fetch_users_with_retry()
print(users)
