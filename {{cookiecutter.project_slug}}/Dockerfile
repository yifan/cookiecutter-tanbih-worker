FROM python:3.6.8-slim
MAINTAINER yifan

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8 PIPENV_HIDE_EMOJIS=1
WORKDIR /code
RUN apt-get update \
    && apt-get install -y \
            librdkafka-dev \
            libxml2-dev \
            libxslt-dev \
            libwebp-dev \
            libmariadb-dev  \
    && rm -rf /var/cache/apk/*

RUN python3 -m ensurepip \
    && rm -rf /usr/lib/python*/ensurepip \
    && pip3 install -U --no-cache-dir pipenv \
    && ln -sf $(which python) /bin/python

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8 PIPENV_HIDE_EMOJIS=1

WORKDIR /code
COPY . /code

RUN python3 -m pip install -r requirements.txt
ENV PYTHONPATH=/code
CMD ["python", "{{cookiecutter.worker_name}}.py"]