# padicwordnet
Demonstration programs for p-adic algorithms on wordnet structures

## Project Setup
This section outlines the steps to set up the project as defined in the Makefile.

- `wordnet.db`: This step creates the `wordnet.db` file using the script `wordnet2padic.py`. To execute this step, run:

  ```
  make wordnet.db
  ```

- `zorgette-catalog.json` and `zorgette-catalog.tex`: These steps create the `zorgette-catalog.json` and `zorgette-catalog.tex` files using the script `create_zorgette_catalogue.py`. Execute these steps with:

  ```
  make zorgette-catalog.json zorgette-catalog.tex
  ```

- `zorgette-results.tex`: This step creates the `zorgette-results.tex` file using the script `multipadic.py`. Run this step with:

  ```
  make zorgette-results.tex
  ```

- `zorgette-ols.tex`: This step generates the `zorgette-ols.tex` file using the script `ols.py`. To execute, use:

  ```
  make zorgette-ols.tex
  ```
