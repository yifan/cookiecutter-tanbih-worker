import logging
from pydantic import BaseModel, Field
from pipeline import {{cookiecutter.worker_type}}Settings, {{cookiecutter.worker_type}}
from version import __worker__, __version__


FORMAT = "%(asctime)-15s %(levelno)s %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('worker')


class Input(BaseModel):
    input_value str = Field(..., title="a string value")


{% if cookiecutter.worker_no_output != 'y' -%}
class Output(BaseModel):
    output_value: str = Field(..., title="a string value")


{% endif -%}
class {{cookiecutter.worker_class_name}}Settings({{cookiecutter.worker_type}}Settings):
    flag: bool = Field(False, title="boolean flag for worker as an example")


class {{cookiecutter.worker_class_name}}({{cookiecutter.worker_type}}):
    def __init__(self):
        settings = {{cookiecutter.worker_class_name}}Settings(
            name=__worker__,
            version=__version__,
            description="worker",
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
        if self.settings.flag:
            text = "flag is on"
        else:
            text = "flag is off"
        return Output(output_value=text)
{% elif cookiecutter.worker_type == 'Producer' %}
    def generate(self):
        if self.settings.flag:
            text = "flag is on"
        else:
            text = "flag is off"
        # Modify this
        yield Output(output_value=text)
{% elif cookiecutter.worker_type == 'Splitter' %}
    def get_topic(self, msg):
        # Modify this
        return msg.get('key', 'default')
{%- endif %}

if __name__ == '__main__':
    worker = {{cookiecutter.worker_class_name}}()
    worker.parse_args()
    worker.start()
