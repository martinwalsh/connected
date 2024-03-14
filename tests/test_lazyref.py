import pytest

from connected.context import Ref, LazyRef


def test_lazy_ref_disconnected():
    input = LazyRef("input")
    assert input.value == Ref.UNRESOLVED


def test_lazy_ref_cycle():
    # This test simulates:
    # context(input=context.output, output=context.input)
    input = LazyRef("input")
    output = LazyRef("output", connected={input})
    input.connect(output)

    with pytest.raises(ValueError) as excinfo:
        input.value
    assert "Cycle detected for attribute 'input'" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        output.value
    assert "Cycle detected for attribute 'output'" in str(excinfo.value)


def test_lazy_ref_simple_resolution():
    # This test simulates:
    # context(
    #   input="Hello, world!",
    #   step=context.input,
    #   output=context.step
    # )

    input = LazyRef("input", _value="Hello, world!")
    step = LazyRef("step", connected={input})
    output = LazyRef("output", connected={step})

    assert input.value == "Hello, world!"
    assert step.value == "Hello, world!"
    assert output.value == "Hello, world!"
