import sqlite3
import functools
from datetime import datetime  # ✅ Add this

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query:
            print(f"[{datetime.now()}] [LOG] Executing SQL Query: {query}")  # ⏱️ Timestamped log
        else:
            print(f"[{datetime.now()}] [LOG] No SQL query found in arguments.")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('ALX_prodev.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Run and fetch
users = fetch_all_users(query="SELECT * FROM user_data")
for user in users:
    print(user)
