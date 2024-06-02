import functools
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
        # if name in self.variables:
        #     raise RuntimeError(f"redefine {name!r}")

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


def rtn_wrapper(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def wrapper(*args):
        # TODO: support keyward arguments
        rtn = fn(*args)
        match rtn:
            case int() | float():
                return NumberValue(rtn)
            case str():
                return StringValue(rtn)
            case bool():
                return BooleanValue(rtn)
            case dict():
                return DictionaryValue({k: rtn_wrapper(v) for k, v in rtn.items()})
            case None:
                return NullValue()
            case _:
                raise NotImplementedError(f"Unknown return type {rtn=!r}")
    return wrapper


def _int(arg: RuntimeValue) -> RuntimeValue:
    match arg:
        case StringValue():
            return int(arg.value)
        case _:
            raise RuntimeError(f"Expected NumberValue, got {arg!r}")


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
    env.declare_variable("print", NativeFnValue(rtn_wrapper(print)), True)
    env.declare_variable("輸入", NativeFnValue(rtn_wrapper(input)), True)
    env.declare_variable("輸出", NativeFnValue(rtn_wrapper(print)), True)
    env.declare_variable("整數", NativeFnValue(rtn_wrapper(_int)), True)

    from datetime import datetime
    env.declare_variable("time", NativeFnValue(rtn_wrapper(datetime.now().timestamp)), True)

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
class DictionaryValue(RuntimeValue):
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

