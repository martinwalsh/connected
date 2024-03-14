from connected.context import Ref, Context


def test_context_keywords_in_constructor():
    assert Context(input="Hello, world!").input.value == "Hello, world!"


def test_context_unresolved_attributes():
    context = Context()
    assert context.input.value == Ref.UNRESOLVED
    assert context.to_dict() == {"input": Ref.UNRESOLVED}


def test_context_resolved_attributes():
    context = Context(input="Hello, world!")
    assert context.input.value == "Hello, world!"
    assert context.to_dict() == {"input": "Hello, world!"}


def test_context_resolve_from_sequential_args():
    context = Context()
    context(input="Hello, world!", output=context.input)
    assert context.to_dict() == {"input": "Hello, world!", "output": "Hello, world!"}


def test_context_resolve_from_reversed_args():
    context = Context()
    context(output=context.input, input="Hello, world!")
    assert context.to_dict() == {"input": "Hello, world!", "output": "Hello, world!"}


def test_context_update_value():
    context = Context(input="Hello, world!")
    assert context.input.value == "Hello, world!"

    context(input="Hello, world, again!")
    assert context.input.value == "Hello, world, again!"


def test_context_updates_propagate():
    context = Context()
    context(input="Hello, world!", output=context.input)
    assert context.to_dict() == {"input": "Hello, world!", "output": "Hello, world!"}

    context(input="Hello, world, again!")
    assert context.to_dict() == {
        "input": "Hello, world, again!",
        "output": "Hello, world, again!",
    }


def test_context_selective_updates_propagate():
    context = Context()
    context(input="Hello, world!", step=context.input, output=context.step)

    assert context.to_dict() == {
        "input": "Hello, world!",
        "step": "Hello, world!",
        "output": "Hello, world!",
    }

    context(step="Hello, world, again!")
    assert context.to_dict() == {
        "input": "Hello, world!",
        "step": "Hello, world, again!",
        "output": "Hello, world, again!",
    }
