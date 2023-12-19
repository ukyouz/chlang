from dataclasses import dataclass


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



