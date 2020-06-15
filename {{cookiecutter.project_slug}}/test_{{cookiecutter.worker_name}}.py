from unittest import TestCase
from {{cookiecutter.worker_name}} import {{cookiecutter.worker_class_name}}


class Test{{cookiecutter.worker_class_name}}(TestCase):
    def test_process(self):
        worker = {{cookiecutter.worker_class_name}}()
        dct = {'processed': False}
        worker.process(dct)
        assert dct['processed'] == True
