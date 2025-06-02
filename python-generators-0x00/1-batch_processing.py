seed = __import__('seed')

def stream_users_in_batches(batch_size):
    """
    Generator that yields user records from the 'user_data' table in batches.
    """
    offset = 0
    while True:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
        rows = cursor.fetchall()
        connection.close()

        if not rows:
            break
        yield rows
        offset += batch_size


def batch_processing(batch_size):
    """
    Generator that yields users (as dicts) with age > 25 from the DB.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            try:
                if int(user['age']) > 25:
                    yield user
            except (ValueError, KeyError):
                continue
