#!/usr/bin/env python3

import nltk
from nltk.corpus import wordnet as wn

largest_number = 0
found_in = ""

def traverse_synset(synset, path=''):
    """
    Traverses the given synset (WordNet node), prints its path and name,
    and recursively traverses its hyponyms (children).
    """
    global largest_number
    global found_in
    # Print the current synset's path and name
    print(f"{path} - {synset.name()}")

    # Recursively traverse each hyponym
    for i, hyponym in enumerate(synset.hyponyms()):
        if i > largest_number:
            largest_number = i
            found_in = hyponym
        traverse_synset(hyponym, path + '.' + str(i + 1))

def main():
    # Start at the top level of WordNet
    entity = wn.synset("entity.n.01")
    traverse_synset(entity,"1")
    #for i, synset in enumerate(wn.all_synsets(pos='n')):
    #    # Only process top-level synsets (those without hypernyms)
    #    if not synset.hypernyms():
    #        traverse_synset(synset, path=str(i + 1))
    print(f"# MAX = {largest_number+1}, in {found_in}")

if __name__ == "__main__":
    main()
