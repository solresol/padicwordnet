#!/usr/bin/env python3

import sqlite3

def convert_path_to_number(p, path):
    # Split the path into parts and reverse it for easy exponent handling
    parts = list(map(int, path.split('.')))[::-1]
    # Calculate the weighted sum using the provided prime number exponentiation
    number = sum(part * (p**i) for i, part in enumerate(parts))
    return number

