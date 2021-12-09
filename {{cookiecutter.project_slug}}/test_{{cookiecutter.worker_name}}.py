from unittest import TestCase
from pydantic import BaseModel
from pipeline import Message
from {{cookiecutter.worker_name}} import {{cookiecutter.worker_class_name}}
from version import __worker__, __version__


class Test{{cookiecutter.worker_class_name}}(TestCase):
    def test_worker(self):
        worker = {{cookiecutter.worker_class_name}}()
{% if cookiecutter.worker_type == 'Processor' %}
        msgs = [{'key': 'msg1'}, {'key': 'msg2'}]
        worker.parse_args(args=['--in-kind', 'MEM',{%- if cookiecutter.worker_no_output == 'n' -%} '--out-kind', 'MEM'{%- endif %}])
        worker.source.load_data(msgs)
        worker.start()
{%- if cookiecutter.worker_no_output == 'n' %}
        # make sure we get two results
        self.assertEqual(len(worker.destination.results), len(msgs))
        result1 = worker.destination.results[0]
        self.assertEqual(result1.get('key'), 'msg1')
{%- endif -%}
{% elif cookiecutter.worker_type == 'Producer' %}
        [msg] = list(worker.generate())
        self.assertTrue(msg.get('key', 'message-id'))
{% elif cookiecutter.worker_type == 'Splitter' %}
        msg = Message(content={'key': 'a'})
        self.assertEqual(worker.get_topic(msg), 'a')
{%- endif %}
