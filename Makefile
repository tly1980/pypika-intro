compile-doc:
	PYTHONPATH=src/ python -m examples > example.md
	cat README-0.md > README.md
	cat example.md >> README.md


test:
	PYTHONPATH=src py.test
