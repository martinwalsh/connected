from enum import Enum
from typing import Any, Self, Literal
from dataclasses import dataclass

from _typeshed import Incomplete

class Ref(Enum):
    UNRESOLVED: int

@dataclass
class LazyRef:
    name: str
    connected: set[Self] = ...
    def connect(self, ref: Self) -> None: ...
    @property
    def value(self) -> Self | Literal[Ref.UNRESOLVED]: ...
    def __eq__(self, other: Any) -> bool: ...
    def __hash__(self) -> int: ...
    def __init__(self, name, connected, _value) -> None: ...

class Context:
    name: Incomplete
    def __init__(self, **kwds: Any) -> None: ...
    def __getattr__(self, name: str) -> LazyRef: ...
    def __call__(self, **kwds: Any) -> Self: ...
    def to_dict(self) -> dict[str, Any]: ...
    def __or__(self, other): ...
    def __ror__(self, other): ...