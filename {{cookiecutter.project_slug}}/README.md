{{cookiecutter.project_name}}
====

{{cookiecutter.project_description}}


## Initialize virtual environment

```
make
```


## Run test

```
make test
```


## Run locally

display help information
```
make run ARGS="--help"
```

Run command with file
```
make run ARGS="--kind FILE --infile input.jsonl --outfile -"
```

Run command with stdin
```
cat input.jsonl | make run ARGS="--kind FILE --infile - --outfile -"
```


## Run docker

Run command with docker
```
cat input.jsonl | docker run -i --rm {{cookiecutter.container_registery}}/{{cookiecutter.worker_name}} \
    --kind FILE --infile - --outfile -
```


## Author
{{cookiecutter.author}}
