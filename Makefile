PYTHON ?= python3

.PHONY: install run test format

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) -m uvicorn app.main:app --reload

test:
	$(PYTHON) -m pytest

format:
	$(PYTHON) -m black .
