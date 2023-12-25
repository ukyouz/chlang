from dataclasses import dataclass
from typing import Callable


@dataclass
class RuntimeValue:
    ...


@dataclass
class NullValue(RuntimeValue):
    ...


@dataclass
class NumberValue(RuntimeValue):
    value: int | float


@dataclass
class BooleanValue(RuntimeValue):
    value: bool


@dataclass
class ObjectValue(RuntimeValue):
    properties: dict[str, RuntimeValue]


@dataclass
class NativeFnValue(RuntimeValue):
    call: Callable # Callable[[list[RuntimeValue], Environment], RuntimeValue]

