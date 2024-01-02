#!/usr/bin/env python

import os
import subprocess
import sqlite3  # noqa: F401

# LaTeX Documentation
def convert_path_to_number(p, path):
    path_parts = path.split('.')
    result = 0
    for i, part in enumerate(path_parts):
        result += int(part) * (p ** i)
    return result


# End of LaTeX Documentation
def generate_latex_documentation():
    # Define the path to the LaTeX documentation file
    latex_file = os.path.join(os.path.dirname(__file__), '..', 'docs', 'create_zorgette_catalogue.tex')
    
    # Generate the LaTeX documentation using subprocess
    subprocess.run(['pandoc', '-s', '-o', latex_file, __file__])
    
generate_latex_documentation()

