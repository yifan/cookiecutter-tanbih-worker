VENV = .venv
PY = python3
VPY = $(VENV)/bin/$(PY)
REQUIREMENTS = requirements.txt
PIPSTR = $(foreach wrd, $(REQUIREMENTS), -r $(wrd))
NAME = {{cookiecutter.worker_name}}

.PHONY: $(VPY)
$(VPY):
	$(PY) -m venv $(VENV) && \
	$(VPY) -m pip install $(PIPSTR)

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

.PHONY: docker
docker: image
	cat fixtures/input.jsonl | \
		docker run -i $(NAME) python {{cookiecutter.worker_name}}.py \
		--in-kind FILE --in-filename - \
		--in-mappings content:text \
		--out-kind FILE --out-filename - \
		--out-content-only

.PHONY: image
TAG ?= latest
image:
	docker build -t $(NAME):$(TAG) -f ./Dockerfile .


.PHONY: clean
clean:
	rm -rf $(VENV)
	find . -name '__pycache__' -delete
