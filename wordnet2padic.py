#!/usr/bin/env python3

import nltk
from nltk.corpus import wordnet as wn
from database import open_database, create_table, delete_entries, save_path

largest_number = 0
found_in = ""

def traverse_synset(synset, path='', connection=None):
    """
    Traverses the given synset (WordNet node), prints its path and name,
    and recursively traverses its hyponyms (children).
    """
    global largest_number
    global found_in
    # Save the current synset's path and name to the database
    save_path(connection, f'{path} - {synset.name()}')

    # Recursively traverse each hyponym
    for i, hyponym in enumerate(synset.hyponyms()):
        if i > largest_number:
            largest_number = i
            found_in = hyponym
        traverse_synset(hyponym, path + '.' + str(i + 1), connection)

def main():
    # Initialize and prepare the database
    connection = open_database()
    create_table(connection)
    delete_entries(connection)

    # Start at the top level of WordNet
    entity = wn.synset("entity.n.01")
    traverse_synset(entity, "1", connection)
    #for i, synset in enumerate(wn.all_synsets(pos='n')):
    #    # Only process top-level synsets (those without hypernyms)
    #    if not synset.hypernyms():
    #        traverse_synset(synset, path=str(i + 1))
    # Commit the changes to the database and close the connection
    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()
