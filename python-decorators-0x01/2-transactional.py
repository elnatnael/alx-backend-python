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

# ✅ Decorator to handle transaction commit/rollback
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("[LOG] Transaction committed.")
            return result
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Transaction rolled back due to: {e}")
            raise
    return wrapper

# ✅ Use proper MySQL placeholders (%s)
@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor()
    cursor.execute("UPDATE user_data SET email = %s WHERE user_id = %s", (new_email, user_id))

# ✅ Run update
update_user_email(user_id='0001ee69-a8ce-4709-b66f-c409d16fd064', new_email='Crawford_Cartwright@hotmail.com')
