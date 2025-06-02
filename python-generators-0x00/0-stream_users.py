def stream_users():
    """
    Generator that reads users from a text file, one line at a time.
    Each line is assumed to represent one user (e.g., JSON string, CSV row, plain name, etc.).
    """
    file_path = 'user_data.csv'  # Make sure this file exists in the same directory

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                yield line.strip()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
