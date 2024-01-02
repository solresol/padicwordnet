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


def random_synset(dbconn: sqlite3.Connection, under_path: str = '1', how_many: int = 1, minimum_hyponyms: int = 1) -> List[Tuple[str, str]]:
    """
    Read the 'synset_paths' table from a SQLite database into a DataFrame.

    Args:
        database_path (str): The file path to the SQLite database.

    Returns:
        pd.DataFrame: The DataFrame containing the 'synset_paths' table.
    """
    cursor = dbconn.cursor()
    params = [f'{under_path}.%', minimum_hyponyms]
    query = f"""select synset_name, path
        from synset_paths
       where path like ?
         and recursive_hyponym_count >= ?"""
    cursor.execute(query, params)
    all_synsets = [(x[0],x[1]) for x in cursor]
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

def errand(dbconn: sqlite3.Connection, good_path: str, bad_path: str, prime: int) -> Dict[str, Union[str, int]]:
    zorgette_request, zorgette_path = random_synset(dbconn, good_path, minimum_hyponyms=100)[0]    
    good_robots = random_synset(dbconn,
                                zorgette_path,
                                minimum_hyponyms=0,
                                how_many=2)
    bad_robot = random_synset(dbconn, bad_path, minimum_hyponyms=0)[0]
    return {
        "Zorgette's Request": zorgette_request,
        "Robot 1's loot": good_robots[0][0],
        "Robot 1's number": convert_path_to_number(prime, good_robots[0][1]),
        "Robot 2's loot": good_robots[1][0],
        "Robot 2's number": convert_path_to_number(prime, good_robots[1][1]),
        "Robot 3's loot": bad_robot[0],
        "Robot 3's number": convert_path_to_number(prime, bad_robot[1])
    }

    
def main():
    import argparse
    import pandas

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--prime', type=int, default=409, help='The prime base for path conversion.')
    parser.add_argument('--database', type=str, default='wordnet.db', help='The database file path.')
    parser.add_argument('--random-seed', type=int, default=51, help='Reproducible output.')
    parser.add_argument('--living-thing-synset', type=str, default='living_thing.n.01', help='What the good robots fetch.')
    parser.add_argument('--object-synset', type=str, default='object.n.01', help='What the bad robots fetch')
    parser.add_argument("--number-of-errands", type=int, default=20, help="How many times Zorgette sent the robots out")
    parser.add_argument("--json-output", type=str, default="zorgette-catalog.json", help="The JSON file to put the output into")
    parser.add_argument("--latex-output", type=str, default="zorgette-catalog.tex", help="The LaTeX file to the the table into")
    #parser.add_argument("--verbose", action="store_true",

    args = parser.parse_args()

    p = args.prime

    random.seed(args.random_seed)
    
    connection = sqlite3.connect(args.database)
    living_things = path_of_synset(connection, args.living_thing_synset)
    everything = path_of_synset(connection, args.object_synset)

    df = pandas.DataFrame.from_records(
        [errand(connection, living_things, everything, args.prime)
         for i in range(args.number_of_errands)]
    )
    df.to_latex(args.latex_output, index=False)

    df = df[["Robot 1's number", "Robot 2's number", "Robot 3's number"]]
    df.columns = ['r1', 'r2', 'r3']
    df.to_json(args.json_output, index=False, orient='values')


if __name__ == '__main__':
    main()

