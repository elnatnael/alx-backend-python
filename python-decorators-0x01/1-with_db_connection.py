import mysql.connector
import functools

# ✅ Decorator to manage MySQL DB connection
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

# ✅ Function that uses automatic DB connection
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data LIMIT 1 OFFSET %s", (user_id - 1,))
    return cursor.fetchone()

# ✅ Fetch user by ID
user = get_user_by_id(user_id=1)
print(user)
