#!/usr/bin/python3

import mysql.connector
import pandas as pd
import uuid

# 🔧 Database configuration
DB_CONFIG = {
    'user': 'root',              # change if needed
    'password': 'messimera12',  # change this to your password
    'host': 'localhost'
}

DB_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'

TABLE_SCHEMA = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    user_id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age INT  NOT NULL,
    INDEX(user_id)
);
"""
insert_stmt = """
INSERT INTO user_data (user_id, name, email, age)
VALUES (%s, %s, %s, %s)
"""

def connect_db():
    """Connect to MySQL server without specifying database."""
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        return cnx
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        return None

def create_database(connection):
    """Create database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")

def connect_to_prodev():
    """Connect to MySQL specifying the ALX_prodev database."""
    try:
        cnx = mysql.connector.connect(database=DB_NAME, **DB_CONFIG)
        return cnx
    except mysql.connector.Error as err:
        print(f"Error connecting to database {DB_NAME}: {err}")
        return None

def create_table(connection):
    """Create user_data table."""
    try:
        cursor = connection.cursor()
        cursor.execute(TABLE_SCHEMA)
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")

def insert_data(connection, csv_file):
    """Insert data from CSV into the user_data table."""
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Failed to read CSV file: {e}")
        return

    if not {'name', 'email', 'age'}.issubset(df.columns):
        print("CSV file must contain 'name', 'email', and 'age' columns.")
        return

    insert_stmt = f"""
    INSERT INTO {TABLE_NAME} (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """

    cursor = connection.cursor()
    for _, row in df.iterrows():
        uid = str(uuid.uuid4())
        try:
            cursor.execute(insert_stmt, (uid, row['name'], row['email'], row['age']))
        except mysql.connector.Error as err:
            print(f"Error inserting row: {err}")
            connection.rollback()
            cursor.close()
            return
    connection.commit()
    cursor.close()
