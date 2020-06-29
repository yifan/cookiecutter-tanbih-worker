from unittest import TestCase
from pipeline import Message
from {{cookiecutter.worker_name}} import {{cookiecutter.worker_class_name}}


class Test{{cookiecutter.worker_class_name}}(TestCase):
{% if cookiecutter.worker_type == 'Processor' %}
    def test_process(self):
        worker = {{cookiecutter.worker_class_name}}()
        msg = Message({'processed': False})
        worker.process(msg)
        self.assertTrue(msg.get('newKey', False))
{% elif cookiecutter.worker_type == 'Generator' %}
    def test_generate(self):
        worker = {{cookiecutter.worker_class_name}}()
        [msg] = list(worker.generate())
        self.assertTrue(msg.get('key', 'message-id'))
{% elif cookiecutter.worker_type == 'Splitter' %}
    def test_get_topic(self):
        worker = {{cookiecutter.worker_class_name}}()
        msg = Message({'key': 'a'})
        self.assertEqual(worker.get_topic(msg), 'a')
{%- endif %}
