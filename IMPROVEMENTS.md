# IMPROVEMENTS.md

*Analysis date: 2026-07-11*

padicwordnet is a small research/demonstration repo (~550 lines of Python) that
extracts hypernym paths from WordNet into a SQLite database
(`wordnet2padic.py` + `database.py`), generates a synthetic "zorgette"
catalogue (`create_zorgette_catalogue.py`), and then fits planes to the data
two ways: a p-adic search (`multipadic.py`, using `padic.py`) and ordinary
least squares (`ols.py`), emitting LaTeX fragments consumed elsewhere. The
repo is quiet (last substantive commits were Sweep-bot Makefile/CI churn in
early 2024), has no tests despite a `test-data/` directory, and carries some
editor backup files and pre-uv packaging.

## Bugs & Fixes

1. **`padic.py: measure()` is off by one.** For `q` not divisible by `prime`
   it returns `1.0` instead of `0` — the p-adic valuation of a unit is 0, so
   `distance()` computes `p^-(v+1)` rather than `p^-v`. Every distance is a
   factor of `p` too small. Rankings/argmins are unaffected (uniform scaling),
   but any absolute distance reported in `zorgette-results.tex` is wrong.
   Fix: `return 0.0` in the unit case (or rename to make the +1 intentional
   and document it).

2. **`padic.py: measure()` can crash on Fractions.** In the Fraction branch,
   `measure(prime, q.numerator) - measure(prime, q.denominator)` will raise
   `TypeError` if the numerator is 0 (`measure` returns `None`). `Fraction`
   normalises 0 to `Fraction(0,1)` which is caught by `q == 0` at the top, so
   it's latent today — but the code path is fragile; make `measure` return
   `math.inf` (or raise) for 0 instead of `None`, and simplify `distance()`.

3. **Makefile `all` target is wrong.** `all: wordnet.db` then runs
   `python wordnet2padic.py` *again* without `--database`, redundantly and
   inconsistently (`python` vs `python3` elsewhere). `all` should just depend
   on the final artefacts: `all: zorgette-results.tex zorgette-ols.tex`.

4. **CI downloads WordNet twice** (`.github/workflows/main.yml` runs
   `nltk.download('wordnet')` and then `make` does it again) and the final
   "Check exit status" step is a no-op — a failing `make` already fails the
   job. Also `actions/checkout@v2` and `setup-python@v2` are deprecated;
   bump to v4/v5.

5. **`ols.py` shadows/duplicates itself**: `ols` is created at module level
   and again inside `ols_fit`; same pattern with the module-level `y, z`
   symbols. Harmless but confusing — pick one (functions) and delete the
   module-level duplicates.

6. **`multipadic.py` imports typing names from another script**
   (`from create_zorgette_catalogue import Tuple/Union/List`), which executes
   that module's argparse-free top level but is still bizarre; import from
   `typing` directly. It also contains a live "Something funny about this...
   there's only one division" comment above `cross_product` — investigate and
   resolve or delete.

## Housekeeping / Modernization

- **Migrate off `requirements.txt` to uv.** Create `pyproject.toml` via
  `uv init` + `uv add pandas nltk sympy jinja2 scikit-learn`, commit
  `pyproject.toml`/`uv.lock`, delete `requirements.txt`, and change the
  Makefile to invoke scripts with `uv run wordnet2padic.py ...` (no
  `uv run python3` indirection). Update the CI workflow to
  `astral-sh/setup-uv` + `uv sync`.
- **Remove committed backup files.** `fmtalgebra.py~`, `multipadic.py~`,
  `ols.py~`, `padic.py~` are tracked in git even though `.gitignore` now has
  `*~` (gitignore doesn't untrack). `git rm --cached *.py~` — and note
  `fmtalgebra.py~` has no non-backup counterpart; recover it as
  `fmtalgebra.py` if it's wanted, otherwise delete.
- **Sweep leftovers**: `sweep.yaml` and `.github/ISSUE_TEMPLATE/sweep-template.yml`
  belong to the defunct Sweep bot; remove them.
- Local dirt not in git (`wordnet.db`, `Untitled.ipynb`, generated `.tex`/
  `.json`) is correctly ignored — fine, but `Untitled.ipynb` should either be
  named and committed or deleted.

## Testing

- There are two JSON fixtures in `test-data/` but **no test files at all**.
  Quick wins: pytest unit tests for `padic.measure`/`padic.distance`
  (units, prime powers, fractions, zero — these would have caught bug #1),
  for `multipadic.cross_product`/`dot_product`/`place_valued`, and a smoke
  test running `multipadic.py --input-file test-data/test-set1.json`.
- Add a `make test` target and run it in CI before the full pipeline (the
  full pipeline is slow because it walks all of WordNet).

## Documentation

- README explains the Makefile targets but never says *what the experiment
  is*: what a "zorgette" is, what hypothesis the p-adic vs OLS comparison
  tests, what prime 409 signifies, and where the generated `.tex` fragments
  get included. Two paragraphs of motivation would make the repo legible in
  a year's time.
- Document the `synset_paths` schema in `database.py` or the README.

## Security

- No secrets or credentials found in the tracked files. The GitHub workflow
  uses no tokens beyond the default. Low risk overall; only note is the
  unpinned deprecated actions (see Bugs #4).

## Quick Wins

1. Fix `measure()` off-by-one and add the pytest covering it.
2. `git rm --cached *.py~` and drop the Sweep config files.
3. `uv init` + `uv add ...`, delete `requirements.txt`, switch Makefile to
   `uv run`.
4. Fix the `all:` Makefile target and bump CI action versions.
