from connected.context import Context


def test_pipeline_pythonic_simple():
    step1 = Context(input="Hello, world!")
    step2 = Context(output=step1.input)

    assert step2.output.value == "Hello, world!"
    assert step1.to_dict() == {"input": "Hello, world!"}
    assert step2.to_dict() == {"output": "Hello, world!"}


def test_pipeline_dsl_simple():
    context = Context()
    pipeline = context(input="Hello, world!") | context(output=context.input)

    assert pipeline.to_dict() == {"input": "Hello, world!", "output": "Hello, world!"}


def test_pipeline_dict_input():
    context = Context()
    pipeline = {"input": "Hello, world!"} | context(output=context.input)

    assert pipeline.to_dict() == {"input": "Hello, world!", "output": "Hello, world!"}
