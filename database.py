import sqlite3
import argparse


def open_database(database_path: str = 'wordnet.db') -> sqlite3.Connection:
    return sqlite3.connect(database_path)

def create_table(connection: sqlite3.Connection) -> None:
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS synset_paths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT,
            synset_name TEXT,
            direct_hyponym_count INTEGER,
            recursive_hyponym_count INTEGER,
            path_length INTEGER
        );
    """)

def delete_entries(connection: sqlite3.Connection) -> None:
    cursor = connection.cursor()
    cursor.execute("DELETE FROM synset_paths;")

def save_path(connection: sqlite3.Connection, path: str, synset_name: str, direct_hyponym_count: int, recursive_hyponym_count: int, path_length: int) -> None:
    cursor = connection.cursor()
    cursor.execute("INSERT INTO synset_paths (path, synset_name, direct_hyponym_count, recursive_hyponym_count, path_length) VALUES (?, ?, ?, ?, ?);", (path, synset_name, direct_hyponym_count, recursive_hyponym_count, path_length))
