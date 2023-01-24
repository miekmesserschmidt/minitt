from dataclasses import dataclass

from typing import TYPE_CHECKING

from .environment import (
    EmptyEnvironment,
    NormalEmptyEnvironment,
    NormalEnvironment,
    Environment,
    NormalUpDeclaration,
    NormalUpVar,
    UpDeclaration,
    UpVar,
)

from .errors import Critical
from .helpers import Name, DeBruijnIndex


from . import values

from .helpers import DeBruijnIndex, Name, NormalBranchClosure

if TYPE_CHECKING:
    from .values import NeutralValue, Value
    from .expressions import Branch, Expression


class NormalExpression:
    pass


@dataclass
class Lambda(NormalExpression):
    env_length: int
    nexpr: NormalExpression


@dataclass
class Pair(NormalExpression):
    a: NormalExpression
    b: NormalExpression


@dataclass
class Constructor(NormalExpression):
    name: Name
    nexpr: NormalExpression


@dataclass
class Pi(NormalExpression):
    base: NormalExpression
    env_length: int
    family: NormalExpression


@dataclass
class Sigma(NormalExpression):
    base: NormalExpression
    env_length: int
    family: NormalExpression


@dataclass
class Function(NormalExpression):
    branch_closure: "NormalBranchClosure"


@dataclass
class Sum(NormalExpression):
    branch_closure: "NormalBranchClosure"


@dataclass
class Unit(NormalExpression):
    pass


@dataclass
class One(NormalExpression):
    pass


@dataclass
class Set(NormalExpression):
    pass


@dataclass
class NeutralExpr(NormalExpression):
    neut: "Neutral"


class Neutral:
    pass


@dataclass
class Variable(Neutral):
    index: DeBruijnIndex  # counting from left of env


@dataclass
class Application(Neutral):
    fn: Neutral
    arg: NormalExpression


@dataclass
class First(Neutral):
    of: Neutral


@dataclass
class Second(Neutral):
    of: Neutral


@dataclass
class NeutralFunction(Neutral):
    n_closure: "NormalBranchClosure"
    scrutinee: Neutral


def generate_var(index: int) -> "Value":
    return values.NeutralValue(values.Variable(index))


def readback_value(env_len: int, value: "Value") -> NormalExpression:
    match value:
        case values.Lambda(clos):
            arg = generate_var(env_len)
            applied = clos.instantiate(arg)
            normal_expr = readback_value(env_len + 1, applied)
            return Lambda(env_len, normal_expr)

        case values.Pair(a, b):
            na = readback_value(env_len, a)
            nb = readback_value(env_len, b)
            return Pair(na, nb)

        case values.Constructor(name, arg):
            narg = readback_value(env_len, arg)
            return Constructor(name, narg)

        case values.Pi(base, fam_cl):
            b = generate_var(env_len)
            fam = fam_cl.instantiate(b)

            nbase = readback_value(env_len, base)
            nfam = readback_value(env_len + 1, fam)

            return Pi(nbase, env_len, nfam)

        case values.Sigma(base, fam_cl):
            b = generate_var(env_len)
            fam = fam_cl.instantiate(b)

            nbase = readback_value(env_len, base)
            nfam = readback_value(env_len + 1, fam)

            return Sigma(nbase, env_len, nfam)

        case values.Function(branch_clos):
            nenv = readback_env(env_len, branch_clos.env)
            nbranch_clos = NormalBranchClosure(branch_clos.branches, nenv)
            return Function(nbranch_clos)

        case values.Sum(branch_clos):
            nenv = readback_env(env_len, branch_clos.env)
            nbranch_clos = NormalBranchClosure(branch_clos.branches, nenv)
            return Sum(nbranch_clos)

        case values.NeutralValue(neut):
            normal_neut = readback_neutral(env_len, neut)
            return NeutralExpr(normal_neut)

        case values.One():
            return One()
        case values.Set():
            return Set()
        case values.Unit():
            return Unit()

        case _:
            raise Critical("readback errors")


def readback_env(index: DeBruijnIndex, env: Environment) -> NormalEnvironment:
    match env:
        case EmptyEnvironment():
            return NormalEmptyEnvironment()

        case UpVar(prev_env, pattern, value):
            nprev_env = readback_env(index, prev_env)
            nexpr = readback_value(index, value)
            return NormalUpVar(nprev_env, pattern, nexpr)

        case UpDeclaration(prev_env, decl):
            nprev_env = readback_env(index, prev_env)
            return NormalUpDeclaration(nprev_env, decl)

        case _:
            raise Critical("env readback error")


def readback_neutral(env_len: int, neut: values.Neutral) -> Neutral:
    match neut:

        case values.Variable(index):
            return Variable(index)

        case values.Application(fn_neut, arg_val):
            fn_norm = readback_neutral(env_len, fn_neut)
            arg_norm = readback_value(env_len, arg_val)
            return Application(fn_norm, arg_norm)

        case values.First(of_val):
            of_norm = readback_neutral(env_len, of_val)
            return First(of_norm)

        case values.Second(of_val):
            of_norm = readback_neutral(env_len, of_val)
            return Second(of_norm)

        case values.NeutralFunction(br_clos, scrut):
            nenv = readback_env(env_len, br_clos.env)
            nbr_clos = NormalBranchClosure(br_clos.branches, nenv)
            nscrut = readback_neutral(env_len, scrut)
            return NeutralFunction(nbr_clos, nscrut)

        case _:
            raise Critical("neutral_readback error")
