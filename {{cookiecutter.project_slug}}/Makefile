VENV = venv
PY = python3
VPY = $(VENV)/bin/$(PY)
REQUIREMENTS = requirements.txt
PIPSTR = $(foreach wrd, $(REQUIREMENTS), -r $(wrd))

.PHONY: $(VPY)
$(VPY): $(VENV)
	$(PY) -m venv $(VENV) && \
	$(VPY) -m pip install -r requirements.txt
		. ./env/bin/activate && python3 -m pip install $(PIPSTR)

.PHONY: test
test: $(VPY)
	$(VPY) -m pytest $(ARGS)

.PHONY: dev
dev: $(VPY)
	$(VPY) ./{{cookiecutter.worker_name}}.py --debug \
		--in-kind FILE --in-filename fixtures/input.jsonl --in-content-only \
		--out-kind FILE --out-filename -

.PHONY: run
run: $(VPY)
	$(VPY) ./{{cookiecutter.worker_name}}.py $(ARGS)
