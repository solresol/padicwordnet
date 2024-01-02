import sqlite3


def open_database():
    return sqlite3.connect("wordnet.db")

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS synset_paths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT
        );
    """)

def delete_entries(connection):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM synset_paths;")

def save_path(connection, path):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO synset_paths (path) VALUES (?);", (path,))
