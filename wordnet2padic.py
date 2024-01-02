#!/usr/bin/env python3
import argparse
import argparse
import sys
import argparse
import argparse
import sys

parser = argparse.ArgumentParser(description='Process WordNet synsets and store in database')
parser.add_argument('--database', help='Path to the database file', default='wordnet.db')
args = parser.parse_args()

import nltk
from nltk.corpus import wordnet as wn
from typing import Optional
from database import open_database, create_table, delete_entries, save_path
import sqlite3
import sqlite3

# TODO: Add type hint: sqlite3.Connection for the 'connection' parameter of the 'create_table' function where it is defined.

largest_number = 0
found_in = ""

def traverse_synset(synset: wn.synset, path: str = '', connection: Optional[sqlite3.Connection] = None):
    """
    Traverses the given synset (WordNet node), stores its path and name in the database,
    and recursively traverses its hyponyms (children).
    """
    global largest_number
    global found_in
    # Save the current synset's path and name to the database
    save_path(connection, path, synset.name())

    # Recursively traverse each hyponym
    for i, hyponym in enumerate(synset.hyponyms()):
        if i > largest_number:
            largest_number = i
            found_in = hyponym
        traverse_synset(hyponym, path + '.' + str(i + 1), connection)

def main() -> None:
    # Open an SQLite database connection at the start of the program
    connection = open_database(args.database)
    # Initialize and prepare the database
    connection = open_database()
    create_table(connection)  # Ensure synset_paths table is created if it doesn't exist
    # Delete any existing entries in the table
    delete_entries(connection)

    # Start at the top level of WordNet
    entity = wn.synset("entity.n.01")
    traverse_synset(entity, "1", connection)
    #for i, synset in enumerate(wn.all_synsets(pos='n')):
    #    # Only process top-level synsets (those without hypernyms)
    #    if not synset.hypernyms():
    #        traverse_synset(synset, path=str(i + 1))
    # Commit the changes to the database
    connection.commit()
    # Close the connection
    connection.close()
if __name__ == "__main__":
    main()
