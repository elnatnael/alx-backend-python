from itertools import islice
import csv

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of user dicts from a CSV file.
    Each batch is a list of dictionaries.
    """
    file_path = 'user_data.csv'

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            while True:
                batch = list(islice(reader, batch_size))
                if not batch:
                    break
                yield batch
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")

def batch_processing(batch_size):
    """
    Generator that yields users (as dicts) with age > 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            try:
                if int(user['age']) > 25:
                    yield user
            except (ValueError, KeyError):
                continue  # Skip malformed rows
