import logging
{%- if cookiecutter.prometheus_enabled == 'y' %}
from prometheus_client import Counter
{%- endif %}
from pipeline import {{cookiecutter.worker_type}}Config, {{cookiecutter.worker_type}}
from version import __worker__, __version__


FORMAT = "%(asctime)-15s %(levelno)s %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('worker')


class {{cookiecutter.worker_class_name}}({{cookiecutter.worker_type}}):
    def __init__(self):
{% if cookiecutter.worker_type == 'Processor' %}
        config = ProcessorConfig()
{%- if cookiecutter.worker_no_output == 'y' %}
        config.disable_output()
{%- endif -%}
{% elif cookiecutter.worker_type == 'Generator' %}
        config = GeneratorConfig()
{% elif cookiecutter.worker_type == 'Splitter' %}
        config = SplitterConfig()
{%- endif %}
        super().__init__(
            __worker__, __version__,
            "{{cookiecutter.project_description}}",
            config,
        )

    def setup(self):
        # Add custom initialization code such as loading models
        # and establish connections here
        pass
{% if cookiecutter.worker_type == 'Processor' %}
    def process(self, msg):
        value = msg.get('existingKey', 1)
        msg.update({
            'existingKey': value+1,
            'processed': True,
        })
        return None
{% elif cookiecutter.worker_type == 'Generator' %}
    def generate(self):
        # Modify this
        yield {'key': 'message-id'}
{% elif cookiecutter.worker_type == 'Splitter' %}
    def get_topic(self, msg):
        # Modify this
        return msg.get('key', 'default')
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
