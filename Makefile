setup-local:
	@if [ ! -d .venv ]; then uv venv; fi
	uv pip install -e .

test-unit: setup-local
	.venv/bin/python -m unittest discover -s tests 