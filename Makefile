.PHONY: rec it test clean

rec:
	python -m src.main recursive --explain

it:
	python -m src.main iterative --explain

test:
	python -m pytest tests/

clean:
	rm -rf __pycache__ src/__pycache__ tests/__pycache__
