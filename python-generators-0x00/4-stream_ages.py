seed = __import__('seed')

def stream_user_ages():
    offset = 0
    batch_size = 100
    while True:
        conn = seed.connect_to_prodev()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT age FROM user_data LIMIT {batch_size} OFFSET {offset}")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            break

        for row in rows:
            try:
                yield int(row['age'])
            except (ValueError, KeyError):
                continue

        offset += batch_size
def compute_average_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    if count == 0:
        print("No valid age data found.")
    else:
        print(f"Average age of users: {total / count:.2f}")

if __name__ == "__main__":
    compute_average_age()
