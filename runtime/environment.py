from dataclasses import dataclass
from dataclasses import field
from typing import Callable
from typing import Self

from frontend.chast import Statement


@dataclass
class RuntimeValue:
    ...


@dataclass
class Environment:
    parent: None | Self = field(default=None)
    variables: dict[str, RuntimeValue] = field(default_factory=dict)
    _consts: set[str] = field(default_factory=set)

    def declare_variable(self, name: str, value: RuntimeValue, is_const:bool=False) -> RuntimeValue:
        if name in self.variables:
            raise RuntimeError(f"redefine {name!r}")

        self.variables[name] = value
        if is_const:
            self._consts.add(name)
        return value

    def assign_variable(self, name: str, value: RuntimeValue) -> RuntimeValue:
        env = self.resolve_var_scope(name)
        if name in env._consts:
            raise RuntimeError(f"reassign const {name!r}")

        env.variables[name] = value
        return value

    def lookup_variable(self, name: str) -> RuntimeValue:
        env = self.resolve_var_scope(name)
        return env.variables[name]

    def resolve_var_scope(self, varname: str) -> Self:
        if varname in self.variables:
            return self

        if self.parent is None:
            raise RuntimeError(f"Undefined {varname!r}")

        return self.parent.resolve_var_scope(varname)


def create_global_env() -> Environment:
    env = Environment()
    # create default global environment
    env.declare_variable("True", BooleanValue(True), True)
    env.declare_variable("False", BooleanValue(False), True)
    env.declare_variable("是", BooleanValue(True), True)
    env.declare_variable("否", BooleanValue(False), True)
    env.declare_variable("Null", NullValue(), True)
    env.declare_variable("空", NullValue(), True)

    # define a native builtin method
    def _print(args, env):
        print(*args)
        return NullValue()
    env.declare_variable("print", NativeFnValue(_print), True)

    def _time(args, env):
        from datetime import datetime
        return NumberValue(datetime.now().timestamp())
    env.declare_variable("time", NativeFnValue(_time), True)

    return env


@dataclass
class NullValue(RuntimeValue):
    ...


@dataclass
class NumberValue(RuntimeValue):
    value: int | float


@dataclass
class StringValue(RuntimeValue):
    value: str


@dataclass
class BooleanValue(RuntimeValue):
    value: bool


@dataclass
class ObjectValue(RuntimeValue):
    properties: dict[str, RuntimeValue]


FunctionCall = Callable[[list[RuntimeValue], Environment], RuntimeValue]
@dataclass
class NativeFnValue(RuntimeValue):
    call: FunctionCall


@dataclass
class FunctionValue(RuntimeValue):
    name: str
    parameters: list[str]
    declaration_env: Environment
    body: list[Statement]

