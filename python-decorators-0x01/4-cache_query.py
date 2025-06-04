import functools
import mysql.connector

query_cache = {}

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


# ✅ Decorator to cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args):
        cache_key = (query, args)
        if cache_key in query_cache:
            print("[CACHE] Returning cached result.")
            return query_cache[cache_key]
        
        print("[DB] Executing query and caching result.")
        result = func(conn, query, *args)
        query_cache[cache_key] = result
        return result
    return wrapper
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM  user_data ")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM  user_data ")
