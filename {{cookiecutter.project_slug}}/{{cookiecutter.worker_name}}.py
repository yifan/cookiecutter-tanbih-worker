import logging
from pydantic import BaseModel, Field
from pipeline import {{cookiecutter.worker_type}}Settings, {{cookiecutter.worker_type}}
from version import __worker__, __version__


FORMAT = "%(asctime)-15s %(levelno)s %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('worker')


{% if cookiecutter.worker_type != 'Producer' -%}
class Input(BaseModel):
    """ Input class definition
        A worker should define the fields needed for worker to function
        here.
    """
    input_value: str = Field(..., title="a string value")

{% endif -%}
{% if cookiecutter.worker_no_output != 'y' -%}
class Output(BaseModel):
    """ Output class definition
    """
    output_value: str = Field(..., title="a string value")


{% endif -%}
class {{cookiecutter.worker_class_name}}Settings({{cookiecutter.worker_type}}Settings):
    """ worker specific settings
        user will be able to set these values in environment variables or command line,
        worker will be able to access it through self.settings
    """
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
        # and establish connections here. This function will be called
        # once when worker instance is created
        pass
{% if cookiecutter.worker_type == 'Processor' %}
    def process(self, input, id_):
        """ process function is called for every input, message_content is a instance
            of Input class defined above.

        """
        if self.settings.flag:
            text = input.input_value
        else:
            text = input.input_value + " flag is off"

        return Output(output_value=text)
{% elif cookiecutter.worker_type == 'Producer' %}
    def generate(self):
        # generate two outputs only
        for i in range(2):
            if self.settings.flag:
                text = "flag is on"
            else:
                text = "flag is off"
            yield Output(output_value=text)
{% elif cookiecutter.worker_type == 'Splitter' %}
    def get_topic(self, msg):
        # Modify this
        return msg.content.get('input_value', 'default')
{%- endif %}

if __name__ == '__main__':
    worker = {{cookiecutter.worker_class_name}}()
    worker.parse_args()
    worker.start()
