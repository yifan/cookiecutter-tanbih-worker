.PHONY: test
init:
	rm -rf venv && python3 -m venv venv && . venv/bin/activate && python3 -m pip install -r requirements.txt
test:
	. venv/bin/activate && python3 -m pytest
pdb:
	. venv/bin/activate && python3 -m pdb ./{{cookiecutter.worker_name}}.py --kind FILE --infile fixtures/articles.json
dev:
	. venv/bin/activate && python3 ./{{cookiecutter.worker_name}}.py --kind FILE --infile fixtures/articles.json --repeat 1 --debug
