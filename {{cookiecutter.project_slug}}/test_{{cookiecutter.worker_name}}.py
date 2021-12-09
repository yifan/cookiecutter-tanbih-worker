from unittest import TestCase
from pipeline import Message
from {{cookiecutter.worker_name}} import {{cookiecutter.worker_class_name}}


class Test{{cookiecutter.worker_class_name}}(TestCase):
{% if cookiecutter.worker_type == 'Processor' %}
    def test_worker(self):
        worker = {{cookiecutter.worker_class_name}}()
        msgs = [{'key': 'msg1'}, {'key': 'msg2'}]
        worker.parse_args(args=['--in-kind', 'MEM'])
        worker.source.load_data(msgs)
        worker.start()
{%- if cookiecutter.worker_no_output == 'y' %}
        # make sure we get two results
        self.assertEqual(len(worker.destination.results), 2)
        result1 = worker.destination.results[0]
        self.assertEqual(result1.get('key'), 'msg1')
{%- endif -%}
{% elif cookiecutter.worker_type == 'Producer' %}
    def test_generate(self):
        worker = {{cookiecutter.worker_class_name}}()
        [msg] = list(worker.generate())
        self.assertTrue(msg.get('key', 'message-id'))
{% elif cookiecutter.worker_type == 'Splitter' %}
    def test_get_topic(self):
        worker = {{cookiecutter.worker_class_name}}()
        msg = Message(content={'key': 'a'})
        self.assertEqual(worker.get_topic(msg), 'a')
{%- endif %}
