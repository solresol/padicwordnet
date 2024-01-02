#!/usr/bin/env python3

import sqlite3

def convert_path_to_number(p: int, path: str) -> int:
    path_parts = path.split('.')
    result = 0
    for i, part in enumerate(path_parts):
        result += int(part) * (p ** i)
    return result


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--prime', type=int, default=409, help='The prime base for path conversion.')
    parser.add_argument('--database', type=str, default='wordnet.db', help='The database file path.')
    parser.add_argument('--random-seed', type=int, default=42, help='Reproducible output.')
    parser.add_argument('--living-thing-synset', type=str, default='living_thing.n.01', help='What the good robots fetch.')
    parser.add_argument('--object-synset', type=str, default='object.n.01', help='What the bad robots fetch')

    args = parser.parse_args()

    p = args.prime
    database_path = args.database


if __name__ == '__main__':
    main()

