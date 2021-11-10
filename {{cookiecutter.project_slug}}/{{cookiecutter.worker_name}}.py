import logging
{%- if cookiecutter.prometheus_enabled == 'y' %}
from prometheus_client import Counter
{%- endif %}
from pydantic import BaseModel, Field
from pipeline import {{cookiecutter.worker_type}}Settings, {{cookiecutter.worker_type}}
from version import __worker__, __version__


FORMAT = "%(asctime)-15s %(levelno)s %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('worker')


class Input(BaseModel):
    text: str = Field(..., title="article text in a single string", min_length=1)


{%- if cookiecutter.worker_no_output != 'y' %}
class Output(BaseModel):
    output: str = Field(..., title="some output")


{%- endif %}
class {{cookiecutter.worker_class_name}}({{cookiecutter.worker_type}}):
    def __init__(self):
{%- if cookiecutter.worker_type == 'Processor' %}
        settings = ProcessorSettings(
{%- elif cookiecutter.worker_type == 'Producer' %}
        settings = ProducerSettings(
{%- elif cookiecutter.worker_type == 'Splitter' %}
        settings = SplitterSettings(
{%- endif %}
            name=__worker__,
            version=__version__,
            description="worker"
        )
        super().__init__(
            settings,
{%- if cookiecutter.worker_type == 'Processor' %}
            input_class=Input,
{%- endif %}
{%- if cookiecutter.worker_no_output == 'y' %}
            output_class=None,
{%- elif cookiecutter.worker_type != 'Splitter' %}
            output_class=Output,
{%- endif %}
        )

    def setup(self):
        # Add custom initialization code such as loading models
        # and establish connections here
        pass
{% if cookiecutter.worker_type == 'Processor' %}
    def process(self, message_content, message_id):
        return Output(output='some value')
{% elif cookiecutter.worker_type == 'Producer' %}
    def generate(self):
        # Modify this
        yield Output(output='some value')
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
    worker.start({%- if cookiecutter.prometheus_enabled == "y" -%} monitoring=True {%- endif %})
