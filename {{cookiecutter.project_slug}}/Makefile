.PHONY: test
init:
	rm -rf env && python3 -m venv env && . ./env/bin/activate && python3 -m pip install -r requirements.txt
test:
	. ./env/bin/activate && python3 -m pytest -v
pdb:
	. ./env/bin/activate && python3 -m pdb ./{{cookiecutter.worker_name}}.py --kind FILE --infile fixtures/articles.json
dev:
	. ./env/bin/activate && python3 ./{{cookiecutter.worker_name}}.py --kind FILE --infile fixtures/articles.json --repeat 1 --debug --outfile -
run:
	. ./env/bin/activate && python3 ./{{cookiecutter.worker_name}}.py $(ARGS)
