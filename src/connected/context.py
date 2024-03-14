from enum import Enum
from uuid import uuid4
from typing import Any, Self, Literal
from dataclasses import field, dataclass


class Ref(Enum):
    UNRESOLVED: int = 0

    def __repr__(self):
        return f"{self.name}"


@dataclass
class LazyRef:
    name: str
    connected: set[Self] = field(default_factory=set, repr=True)
    _value: Any = field(default=Ref.UNRESOLVED, repr=True)

    def connect(self, ref: Self) -> None:
        self.connected.add(ref)

    @property
    def value(self) -> Self | Literal[Ref.UNRESOLVED]:
        return self._resolve()

    def _resolve(self, visited: set | None = None):
        if self._value is not Ref.UNRESOLVED:
            return self._value

        if not self.connected:
            return Ref.UNRESOLVED

        if visited is None:
            visited = set()
        visited.add(self)

        for ref in self.connected:
            if ref in visited:
                raise ValueError(f"Cycle detected for attribute '{ref.name}'")
            return ref._resolve(visited)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, LazyRef) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class Context:
    def __init__(self, **kwds: Any):
        self.name: str = uuid4().hex[:8]
        self._refs: dict[str, LazyRef] = {}
        if kwds:
            self.__call__(**kwds)

    def __repr__(self) -> str:
        return f"Context<{tuple(self._refs)} [{self.name}]>"

    def __getattr__(self, name: str) -> LazyRef:
        # Create a new `LazyRef` if the `name` is referenced before it exists.
        if name not in self._refs:
            self._refs[name] = LazyRef(name)
        return self._refs[name]

    def __call__(self, **kwds: Any) -> Self:
        for name, value in kwds.items():
            ref = self._refs.get(name)
            match ref, value:
                case (LazyRef(), LazyRef()):
                    # Intermediate node: resolves a LazyRef through another.
                    # ex. `step` in context(input="", step=context.input, output=context.step)
                    # Connect `ref` to `value`.
                    ref.connect(value)  # type: ignore
                case (LazyRef(), _):
                    # Starting node: resolves a LazyRef to a concrete value.
                    # ex. `input` in context(input="Hello, world!", output=context.input)
                    # Update `_value` on `ref`, set it to `value`.
                    ref._value = value  # type: ignore
                case (None, LazyRef()):
                    # Ending node: resolves a LazyRef through another.
                    # ex. `output` in context(input="Hello, world!", output=context.input)
                    # Create a new `LazyRef` pre-connected with `value`.
                    self._refs[name] = LazyRef(name, connected={value})
                case (None, _):
                    # Not yet a graph?: value found without a corresponding LazyRef.
                    # ex. context(input="Hello, world!")
                    # Create a new `LazyRef` with `value` as its `_value`.
                    self._refs[name] = LazyRef(name, _value=value)
                case _:
                    raise ValueError("Unrecognized argument type")
        return self

    def to_dict(self) -> dict[str, Any]:
        return {name: ref.value for name, ref in self._refs.items()}

    def __or__(self, other):
        match other:
            case Context():
                return other(**self.to_dict())
            case list():
                for context in other:
                    if not isinstance(context, Context):
                        raise TypeError(f"Unsupported type: {type(context)}")
                    context(**self.to_dict())
                return other
            case _:
                raise TypeError(f"Unsupported type: {type(other)}")

    def __ror__(self, other):
        match other:
            case Context():
                return self(**other.to_dict())
            case dict():
                return self(**other)
            case _:
                raise TypeError(f"Unsupported type: {type(other)}")
