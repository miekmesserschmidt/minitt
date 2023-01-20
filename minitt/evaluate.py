
from typing import TYPE_CHECKING
from .helpers import BranchClosure
from .closure import Closure
from .errors import Critical



if TYPE_CHECKING:
    from .values import Value
    from .environment import Environment
    from .expressions import Expression

def evaluate(expr: "Expression", env: "Environment") -> "Value":
    from . import expressions, values
    from .environment import UpDeclaration
    match expr:
        case expressions.Program(decl, next_expr):
            return evaluate(next_expr, UpDeclaration(env, decl))
        case expressions.Lambda(pattern, binder):
            return values.Lambda(Closure(pattern, binder, env))

        case expressions.Pi(pattern, base, family):
            base_val = evaluate(base, env)
            family_closure = Closure(pattern, family, env)
            return values.Pi(base_val, family_closure)

        case expressions.Application(fn, arg):
            fn_val = evaluate(fn, env)
            arg_val = evaluate(arg, env)
            return apply(fn_val, arg_val)

        case expressions.Sigma(pattern, base, family):
            base_val = evaluate(base, env)
            family_closure = Closure(pattern, family, env)
            return values.Sigma(base_val, family_closure)

        case expressions.Pair(a, b):
            a_val = evaluate(a, env)
            b_val = evaluate(b, env)
            return values.Pair(a_val, b_val)

        case expressions.First(of):
            of_val = evaluate(of, env)
            return first(of_val)

        case expressions.Second(of):
            of_val = evaluate(of, env)
            return second(of_val)

        case expressions.Constructor(name, expr):
            v = evaluate(expr, env)
            return values.Constructor(name, v)

        case expressions.Sum(branches):
            return values.Sum(BranchClosure(branches, env))

        case expressions.Function(branches):
            return values.Function(BranchClosure(branches, env))

        case expressions.Variable(name):
            return env[name]

        case expressions.One():
            return values.One()

        case expressions.Unit():
            return values.Unit()

        case expressions.Set():
            return values.Set()
        case _:
            raise Critical("evaluation error")


def first(of: "Value") -> "Value":
    from . import values
    match of:
        case values.Pair(a,_):
            return a
        case values.NeutralValue(neut):
            n = values.First(neut)
            return values.NeutralValue(n)
        case _:
            raise Critical("first error")
        


def second(of: "Value") -> "Value":
    from . import values
    match of:
        case values.Pair(_,b):
            return b
        case values.NeutralValue(neut):
            n = values.Second(neut)
            return values.NeutralValue(n)
        case _:
            raise Critical("second error")


def apply(fn_val: "Value", arg: "Value") -> "Value":
    from . import values
    match fn_val, arg:
        case (values.Lambda(cl), Value()):
            return cl.instantiate(arg)
        case (
            values.Function(branch_closure),
            values.Constructor(constr_name, constr_arg),
        ):
            fn_val = evaluate(branch_closure[constr_name], branch_closure.env)
            return apply(fn_val, constr_arg)

        case (values.Function(branch_closure), values.NeutralValue(neutral)):
            n = values.NeutralFunction(branch_closure, neutral)
            return values.NeutralValue(n)

        case (values.NeutralValue(neutral_fn), Value()):
            n = values.Application(neutral_fn, arg)
            return values.NeutralValue(n)
        
        case _:
            raise Critical("apply error")
