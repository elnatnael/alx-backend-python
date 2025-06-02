#!/usr/bin/python3
seed = __import__('seed')

def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_pagination(page_size):
    """
    Generator that lazily fetches pages from the database.
    Each page is a list of user records.

    Args:
        page_size (int): Number of users per page

    Yields:
        list: A page of users from the database
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
