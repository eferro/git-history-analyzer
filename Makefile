setup-local:
	@if [ ! -d .venv ]; then uv venv; fi
	uv pip install -e .

test-unit: setup-local
	python3.12 -m unittest discover -s tests 