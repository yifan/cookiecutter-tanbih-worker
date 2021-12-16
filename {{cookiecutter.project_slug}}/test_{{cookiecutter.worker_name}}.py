from unittest import TestCase
from pydantic import BaseModel
from pipeline import Message
from {{cookiecutter.worker_name}} import {{cookiecutter.worker_class_name}}
from version import __worker__, __version__


class Test{{cookiecutter.worker_class_name}}(TestCase):
    def test_worker(self):
        worker = {{cookiecutter.worker_class_name}}()
{% if cookiecutter.worker_type == 'Processor' %}
        msgs = [{'input_value': 'msg1'}, {'input_value': 'msg2'}]
        worker.parse_args(args=['--in-kind', 'MEM',{%- if cookiecutter.worker_no_output == 'n' -%} '--out-kind', 'MEM'{%- endif %}])
        worker.source.load_data(msgs)
        worker.start()
{%- if cookiecutter.worker_no_output == 'n' %}
        # make sure we get two results
        assert len(worker.destination.results) == len(msgs)
        result1 = worker.destination.results[0]
        assert result1.content.get('output_value') == 'msg1 flag is off'
{%- endif -%}
{% elif cookiecutter.worker_type == 'Producer' %}
        worker.parse_args(args='--out-kind MEM'.split())
        worker.start()
        assert len(worker.destination.results) == 2
        assert worker.destination.results[0].content['output_value'] == 'flag is off'
{% elif cookiecutter.worker_type == 'Splitter' %}
        worker.parse_args(args='--in-kind MEM --out-kind MEM'.split())
        worker.source.load_data([{"input_value": "a"}, {"input_value": "b"}])
        worker.start()
        assert len(worker.destinations["a"].results) == 1
        assert len(worker.destinations["b"].results) == 1
{%- endif %}
