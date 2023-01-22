from .declarations import Declaration, Definition, RecursiveDefinition
from .closure import ClosureComposition

from .errors import Critical, NotEqual
from .helpers import lookup
from .normal_forms import (
    NormalExpression,
    generate_var,
    readback_neutral,
    readback_value,
)
from .evaluate import evaluate, first
from .expressions import (
    Application,
    Constructor,
    Expression,
    First,
    Function,
    Lambda,
    Pair,
    Pi,
    Program,
    Second,
    Sigma,
    Set,
    Sum,
    Unit,
    One,
    Variable,
)
from .type_env import TypeEnvironment, type_env_lookup, up_type_environment
from .environment import Environment, UpDeclaration, UpVar

from . import values


def check_type(
    env_len: int, env: Environment, type_env: TypeEnvironment, expr: Expression
):
    match expr:
        case Pi(pattern, base, fam) | Sigma(pattern, base, fam):
            check_type(env_len, env, type_env, base)
            fam_val = evaluate(fam, env)
            v = generate_var(env_len)
            gamma1 = up_type_environment(type_env, pattern, fam_val, v)
            env1 = UpVar(env, pattern, v)
            check_type(env_len + 1, env1, gamma1, fam)

        case Set():
            return
        case other:
            check(env_len, env, type_env, other, values.Set())


def check(
    env_len: int,
    env: Environment,
    type_env: TypeEnvironment,
    expr: Expression,
    type_val: values.Value,
):
    match expr, type_val:
        case Lambda(p, expr), values.Pi(base_val, fam_cl):
            v = generate_var(env_len)
            gamma1 = up_type_environment(type_env, p, base_val, v)
            env1 = UpVar(env, p, v)
            check(env_len + 1, env1, gamma1, expr, fam_cl.instantiate(v))

        case Pair(a, b), values.Sigma(base_val, fam_cl):
            check(env_len, env, type_env, a, base_val)
            a_val = evaluate(a, env)
            check(env_len, env, type_env, b, fam_cl.instantiate(a_val))

        case Constructor(name, expr), values.Sum(br_clos):
            branch_expr = lookup(name, br_clos.branches)
            branch_val = evaluate(branch_expr, env)
            check(env_len, env, type_env, branch_expr, branch_val)

        case Function(branches), values.Pi(values.Sum(br_clos), fam_cl):
            val_branches = br_clos.branches
            if len(branches) == len(val_branches):
                raise Critical("branch length mismatch")

            for br0, br1 in zip(branches, val_branches):
                if br0.name != br1.name:
                    raise Critical("branch name mismatch")

            for br0, br1 in zip(branches, val_branches):
                base_val = evaluate(br1.expr, env)
                ext_fam_cl = ClosureComposition(fam_cl, br0.name)
                br_pi_val = values.Pi(base_val, ext_fam_cl)

                check(env_len, env, type_env, br0.expr, br_pi_val)

        case (Pi(pattern, base, fam) | Sigma(pattern, base, fam)), values.Set():
            check(env_len, env, type_env, base, values.Set())
            v = generate_var(env_len)
            a_val = evaluate(base, env)
            gamma1 = up_type_environment(type_env, pattern, a_val, v)
            env1 = UpVar(env, pattern, v)
            check(env_len + 1, env1, gamma1, fam, values.Set())

        case Sum(branches), values.Set():
            for br in branches:
                check(env_len, env, type_env, br.expr, values.Set())

        case Program(decl, next_expr), type_val:
            gamma1 = check_declaration(env_len, env, type_env, decl)
            env1 = UpDeclaration(env, decl)
            check(env_len, env1, gamma1, next_expr, type_val)

        case ((Unit(), values.One()) | (One(), values.Set())):
            return

        case expr, type_val:
            t1 = check_i(env_len, env, type_env, expr)
            equal_normal_form(env_len, type_val, t1)


def check_i(
    env_len: int, env: Environment, type_env: TypeEnvironment, expr: Expression
) -> values.Value:
    match expr:
        case Variable(name):
            return type_env_lookup(name, type_env)
        case Application(fn, arg):
            t1 = check_i(env_len, env, type_env, fn)
            match t1:
                case values.Pi(base_val, fam_cl):
                    check(env_len, env, type_env, arg, base_val)
                    arg_val = evaluate(arg, env)
                    return fam_cl.instantiate(arg_val)
                case _:
                    raise Critical("application check i error")

        case First(of_):
            t = check_i(env_len, env, type_env, of_)
            match t:
                case values.Sigma(base_val, _):
                    return base_val
                case _:
                    raise Critical("first check i error")

        case Second(of_):
            t = check_i(env_len, env, type_env, of_)
            match t:
                case values.Sigma(_, fam_cl):
                    of_val = evaluate(of_, env)
                    base_val = first(of_val)
                    return fam_cl.instantiate(base_val)
                case _:
                    raise Critical("first check i error")

        case _:
            raise Critical("check_i error")


def check_declaration(
    env_len: int, env: Environment, type_env: TypeEnvironment, decl: Declaration
) -> TypeEnvironment:
    match decl:
        case Definition(pattern, of_type, assignment):
            check_type(env_len, env, type_env, of_type)

            t = evaluate(of_type, env)
            check(env_len, env, type_env, assignment, t)

            ass_val = evaluate(assignment, env)
            return up_type_environment(type_env, pattern, t, ass_val)

        case RecursiveDefinition(pattern, of_type, assignment) as recd:
            check_type(env_len, env, type_env, of_type)

            t = evaluate(of_type, env)
            fresh = generate_var(env_len)
            gamma1 = up_type_environment(type_env, pattern, t, fresh)
            env1 = UpVar(env, pattern, fresh)
            check(env_len + 1, env1, gamma1, assignment, t)

            ass_val = evaluate(assignment, UpDeclaration(env, recd))
            return up_type_environment(type_env, pattern, t, ass_val)

        case _:
            raise Critical("check decl error")


def equal_normal_form(env_len: int, v0: values.Value, v1: values.Value):
    n0 = readback_value(env_len, v0)
    n1 = readback_value(env_len, v1)

    if n0 != n1:
        raise NotEqual()