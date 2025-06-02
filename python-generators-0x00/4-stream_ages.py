#!/usr/bin/python3
seed = __import__('seed')

def stream_user_ages(batch_size=100):
    offset = 0
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
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No valid age data found.")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")

if __name__ == "__main__":
    compute_average_age()
