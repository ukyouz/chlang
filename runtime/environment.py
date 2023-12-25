from dataclasses import dataclass
from dataclasses import field
from typing import Self

from runtime.values import BooleanValue
from runtime.values import NativeFnValue
from runtime.values import NullValue
from runtime.values import NumberValue
from runtime.values import RuntimeValue


@dataclass
class Environment:
    _parent: None | Self = field(default=None)
    _variables: dict[str, RuntimeValue] = field(default_factory=dict)
    _consts: set[str] = field(default_factory=set)

    def declare_variable(self, name: str, value: RuntimeValue, is_const:bool=False) -> RuntimeValue:
        if name in self._variables:
            raise RuntimeError(f"redefine {name!r}")

        self._variables[name] = value
        if is_const:
            self._consts.add(name)
        return value

    def assign_variable(self, name: str, value: RuntimeValue) -> RuntimeValue:
        env = self.resolve_var_scope(name)
        if name in env._consts:
            raise RuntimeError(f"reassign const {name!r}")

        env._variables[name] = value
        return value

    def lookup_variable(self, name: str) -> RuntimeValue:
        env = self.resolve_var_scope(name)
        return env._variables[name]

    def resolve_var_scope(self, varname: str) -> Self:
        if varname in self._variables:
            return self

        if self._parent is None:
            raise RuntimeError(f"Undefined {varname!r}")

        return self._parent.resolve_var_scope(varname)


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
