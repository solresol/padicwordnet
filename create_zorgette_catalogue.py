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
    parser.add_argument('--prime', type=int, default=403, help='The prime base for path conversion.')
    parser.add_argument('--database', type=str, default='wordnet.db', help='The database file path.')

    args = parser.parse_args()

    p = args.prime
    database_path = args.database


if __name__ == '__main__':
    main()

