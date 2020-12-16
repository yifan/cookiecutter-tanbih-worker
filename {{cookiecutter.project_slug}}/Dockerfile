FROM python:3.8-slim
LABEL maintainer={{cookiecutter.author}}

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8 PIPENV_HIDE_EMOJIS=1
RUN apt-get update \
    && apt-get install -y \
            librdkafka-dev \
            libxml2-dev \
            libxslt-dev \
            libwebp-dev \
            libmariadb-dev  \
            gcc \
    && rm -rf /var/cache/apk/*

RUN python3 -m ensurepip \
    && rm -rf /usr/lib/python*/ensurepip \
    && python3 -m pip install -U --no-cache-dir pip \
    && ln -sf $(which python) /bin/python

WORKDIR /code
COPY requirements.txt /code
RUN python3 -m pip install -r /code/requirements.txt

COPY . /code
ENV PYTHONPATH=/code
CMD ["python", "{{cookiecutter.worker_name}}.py"]
