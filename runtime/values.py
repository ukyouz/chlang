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
