#!/usr/bin/env python3

import sqlite3
import json
import random
from typing import List, Tuple, Dict, Union

def convert_path_to_number(p: int, path: str) -> int:
    """
    Convert a dotted path string to a numeric value using the specified p-adic conversion.

    Args:
        p (int): The prime base for path conversion.
        path (str): The dotted path string to convert.

    Returns:
        int: The numeric value of the path.
    """
    path_parts = path.split('.')
    result = 0
    for i, part in enumerate(path_parts):
        result += int(part) * (p ** i)
    return result


def random_synset(dbconn: sqlite3.Connection, under_path: str = '1', how_many: int = 1, minimum_hyponyms: int = 1, maximum_hyponyms : int = 1000000, only_immediately_under_path: bool = False ) -> List[Tuple[str, str]]:
    """
    Read the 'synset_paths' table from a SQLite database into a DataFrame.

    Args:
        database_path (str): The file path to the SQLite database.

    Returns:
        pd.DataFrame: The DataFrame containing the 'synset_paths' table.
    """
    cursor = dbconn.cursor()
    params = [f'{under_path}.%', minimum_hyponyms, maximum_hyponyms]
    query = f"""select synset_name, path
        from synset_paths
       where path like ?
         and direct_hyponym_count >= ?
         and direct_hyponym_count <= ?
    """
    cursor.execute(query, params)
    all_synsets = [(x[0],x[1]) for x in cursor]
    if only_immediately_under_path:
        lup = len(under_path)+1
        #temp_synsets = []
        #for (name,path) in all_synsets:
        #    tail = path[lup:]
        #    print(name,path,tail)
        def is_under_path(x):
            return len(x[lup:].split('.')) == 1
        temp_synsets = [(name,path) for (name,path) in all_synsets if is_under_path(path)]
        #print(under_path, lup, len(temp_synsets), all_synsets)
        all_synsets = temp_synsets
    cursor.close()
    return random.sample(all_synsets, k=how_many)


def path_of_synset(dbconn: sqlite3.Connection, synset_name: str) -> str:
    cursor = dbconn.cursor()
    cursor.execute("select path from synset_paths where synset_name = ? limit 1",
                   [synset_name])
    row = cursor.fetchone()
    if row is None:
        cursor.close()
        raise IndexError(synset_name)
    path = row[0]
    cursor.close()
    return path

def synset_of_path(dbconn: sqlite3.Connection, path: str) -> str:
    cursor = dbconn.cursor()
    cursor.execute("select synset_name from synset_paths where path = ? limit 1",
                   [path])
    row = cursor.fetchone()
    if row is None:
        cursor.close()
        raise IndexError(path)
    synset_name = row[0]
    cursor.close()
    return synset_name    

def errand(dbconn: sqlite3.Connection, good_path: str, bad_path: str, prime: int) -> Dict[str, Union[str, int]]:
    #zorgette_path = good_path
    #zorgette_request = synset_of_path(dbconn, zorgette_path)
    #print(zorgette_path, zorgette_request)
    zorgette_request, zorgette_path = random_synset(dbconn, good_path, only_immediately_under_path=True, minimum_hyponyms=2)[0]
    good_robots = random_synset(dbconn,
                                zorgette_path,
                                minimum_hyponyms=0,
                                how_many=2,
                                only_immediately_under_path=True)
    bad_robot = random_synset(dbconn, bad_path, minimum_hyponyms=0)[0]
    return {
        "Zorgette's Request": zorgette_request,
        #"Zorgette's Path": zorgette_path,
        "Robot 1's loot": good_robots[0][0],
        "Robot 1's loot number": convert_path_to_number(prime, good_robots[0][1]),
        #"Robot 1's Path": good_robots[0][1],
        "Robot 2's loot": good_robots[1][0],
        "Robot 2's loot number": convert_path_to_number(prime, good_robots[1][1]),
        #"Robot 2's Path": good_robots[1][1],
        "Robot 3's loot": bad_robot[0],
        "Robot 3's loot number": convert_path_to_number(prime, bad_robot[1])
    }

    
def main():
    import argparse
    import pandas

    parser = argparse.ArgumentParser(description="Simulate Zorgette's collection process.")
    parser.add_argument('--prime', type=int, default=409, help='The prime base for path conversion.')
    parser.add_argument('--database', type=str, default='wordnet.db', help='The database file path.')
    parser.add_argument('--random-seed', type=int, default=51, help='Reproducible output.')
    #parser.add_argument('--living-thing-synset', type=str, default='living_thing.n.01', help='What the good robots fetch.')
    #parser.add_argument('--living-thing-synset', type=str, default='animal.n.01', help='What the good robots fetch.')
    #parser.add_argument('--living-thing-synset', type=str, default='bovid.n.01', help='What the good robots fetch.')
    #parser.add_argument('--living-thing-synset', type=str, default='mammal_genus.n.01', help='What the good robots fetch.')
    parser.add_argument('--living-thing-synset', type=str, default='tree.n.01', help='What the good robots fetch.')     
    parser.add_argument('--object-synset', type=str, default='object.n.01', help='What the bad robots fetch')
    parser.add_argument("--number-of-errands", type=int, default=10, help="How many times Zorgette sent the robots out")
    parser.add_argument("--json-output", type=str, default="zorgette-catalog.json", help="The JSON file to put the output into")
    parser.add_argument("--latex-output", type=str, default="zorgette-catalog.tex", help="The LaTeX file to the the table into")
    #parser.add_argument("--verbose", action="store_true",

    args = parser.parse_args()

    p = args.prime

    random.seed(args.random_seed)
    
    connection = sqlite3.connect(args.database)
    living_things = path_of_synset(connection, args.living_thing_synset)
    everything = path_of_synset(connection, args.object_synset)

    errand_records = []
    requests_handled = set()
    while len(errand_records) < args.number_of_errands:
        this_errand = errand(connection, living_things, everything, args.prime)
        if this_errand["Zorgette's Request"] in requests_handled:
            continue
        requests_handled.update([this_errand["Zorgette's Request"]])
        errand_records.append(this_errand)
    df = pandas.DataFrame.from_records(errand_records)
    latex_df = pandas.DataFrame()
    for c in [ "Zorgette's Request", "Robot 1's loot", "Robot 2's loot", "Robot 3's loot"]:
        latex_df[c] = df[c].str.replace('_', r'\allowbreak\_')
        if c.startswith("Robot"):
            latex_df[c] = r'{\bf ' + latex_df[c] + r"} \newline " + df[c + " number"].map(str)
    latex_df.to_latex(args.latex_output, index=False,
                      column_format='p{18mm}' + ('p{43mm}' * 3))

    json_df = df[["Robot 1's loot number", "Robot 2's loot number", "Robot 3's loot number"]].copy()
    json_df.to_json(args.json_output, index=False, orient='values')

if __name__ == '__main__':
    main()

