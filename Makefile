all: wordnet.db
	python -m nltk.downloader wordnet
	python wordnet2padic.py

wordnet.db: wordnet2padic.py
	python3 wordnet2padic.py --database wordnet.db

zorgette-catalog.json zorgette-catalog.tex: create_zorgette_catalogue.py wordnet.db
	python3 create_zorgette_catalogue.py --database wordnet.db --json-output zorgette-catalog.json --latex-output zorgette-catalog.tex

zorgette-results.tex: zorgette-catalog.json multipadic.py
	python3 multipadic.py --input-file zorgette-catalog.json --output zorgette-results.tex

zorgette-ols.tex: zorgette-catalog.json ols.py
	python3 ols.py --input-file zorgette-catalog.json --output zorgette-ols.tex
