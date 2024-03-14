from jinja2 import Template as JT

from connected.context import Context, LazyRef


class Template(Context):
    def __init__(self, template: str):
        super().__init__(template=template)

    def render(self):
        return self(prompt=JT(self.template.value).render(**self.to_dict()))


class Retriever(Context):
    _data = {
        "Say hello": "Hello, world!",
        "Say something random": "random",
    }

    def query(self):
        return self(result=self._data[self.question.value])


def test_subclasses_work_like_the_base_class():
    template = Template("{{ result }}")
    retriever = Retriever()

    pipeline = (({"question": "Say hello"} | retriever).query() | template).render()

    assert pipeline.prompt.value == "Hello, world!"
