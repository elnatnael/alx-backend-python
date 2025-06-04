import mysql.connector
import functools

# ✅ Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query:
            print(f"[LOG] Executing SQL Query: {query}")
        else:
            print("[LOG] No SQL query found in arguments.")
        return func(*args, **kwargs)
    return wrapper

# ✅ Connect and fetch from MySQL
@log_queries
def fetch_all_users(query):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="messimera12",
        database="alx_prodev"
    )
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# ✅ Call the function and print results
users = fetch_all_users(query="SELECT * FROM user_data")

for user in users:
    print(user)
