import logging
{%- if cookiecutter.prometheus_enabled == 'y' %}
from prometheus_client import Counter
{%- endif %}
from pipeline import {{cookiecutter.worker_type}}
from version import __worker__, __version__


FORMAT = "%(asctime)-15s %(levelno)s %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('worker')


class {{cookiecutter.worker_class_name}}({{cookiecutter.worker_type}}):
    def __init__(self):
        super().__init__(
            __worker__, __version__,
            "{{cookiecutter.project_description}}",
{%- if cookiecutter.worker_no_output == 'y' %}
            nooutput=True, 
{%- endif -%}
        )
{% if cookiecutter.worker_type == 'Processor' %}
    def process(self, dct):
        # Modify this
        return None
{% elif cookiecutter.worker_type == 'Generator' %}
    def generate(self):
        # Modify this
        yield {'key': 'message-id'}
{% elif cookiecutter.worker_type == 'Splitter' %}
    def get_topic(self, dct):
        # Modify this
        {%- raw %}
        return "{}-{}".format(self.destination.topic, dct.get('key', 'default'))
        {%- endraw %}
{%- endif %}

if __name__ == '__main__':
    worker = {{cookiecutter.worker_class_name}}()
    worker.parse_args()
    if worker.options.debug:
        logger.setLevel(logging.DEBUG)
{%- if cookiecutter.worker_retry == 'y' %}
    worker.use_retry_topic()
{%- endif %}
    worker.start({%- if cookiecutter.prometheus_enabled == "y" -%} monitoring=True {%- endif %})
