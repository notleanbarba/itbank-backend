init: install install-cli

venv:
	python3 -m venv .venv

install: venv
	. .venv/bin/activate; \
	pip install -r requirements.txt; \

build: install
	. .venv/bin/activate; \
	python3 -m build; \
