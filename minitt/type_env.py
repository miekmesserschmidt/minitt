from typing import Dict, TypeAlias
from .evaluate import first, second
from .pattern import EmptyPattern, PairPattern, Pattern, VariablePattern
from .errors import Critical
from .values import Value
from .helpers import Name
from . import values


TypeEnvironment: TypeAlias = Dict[Name, Value]


def make_empty_type_env() -> TypeEnvironment:
    return {}


def type_env_lookup(name: Name, type_env: TypeEnvironment) -> Value:
    return type_env[name]


def up_type_environment(
    type_env: TypeEnvironment, pattern: Pattern, type_val: Value, val: Value
) -> TypeEnvironment:
    match pattern, type_val:
        case (EmptyPattern(), _):
            return type_env

        case (VariablePattern(name), _):
            return {name: type_val} | type_env

        case (PairPattern(a_pattern, b_pattern), values.Sigma(base_val, fam_cl)):
            a = first(val)
            gamma1 = up_type_environment(type_env, a_pattern, base_val, a)

            b_type_val = fam_cl.instantiate(a)
            b = second(val)

            return up_type_environment(gamma1, b_pattern, b_type_val, b)

        # case (MultiPattern((a_pattern, *_)) as multi_pattern, values.Sigma(base_val, fam_cl)):
        #     a = first(val)
        #     gamma1 = up_type_environment(type_env, a_pattern, base_val, a)

        #     b_type_val = fam_cl.instantiate(a)
        #     b = second(val)

        #     return up_type_environment(gamma1, multi_pattern.rest(), b_type_val, b)

        case _:
            raise Critical("up_type_env error")
