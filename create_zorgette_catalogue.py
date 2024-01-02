#!/usr/bin/env python3

import sqlite3

def convert_path_to_number(p: int, path: str) -> int:
    path_parts = path.split('.')
    result = 0
    for i, part in enumerate(path_parts):
        result += int(part) * (p ** i)
    return result




