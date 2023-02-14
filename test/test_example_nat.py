from minitt.environment import EmptyEnvironment
from minitt.checking import check
from minitt.evaluate import evaluate
from minitt.expressions import (
    Application,
    build_arrow_type,
    build_arrow_type,
    Branch,
    Constructor,
    Function,
    Lambda,
    Top,
    Pi,
    Program,
    Set,
    Sum,
    Star,
    Variable,
)

from minitt.pattern import EmptyPattern, VariablePattern
from minitt.declarations import Definition, RecursiveDefinition

from minitt import values
from minitt.type_env import  make_empty_type_env

from lib.helpers import apply, build_program, lam
import lib.nat as N


def test_nat():

    p = build_program(N.nat)
    check(0, EmptyEnvironment(), make_empty_type_env(), p, values.Top())


def test_nat_elim():

    p = build_program(N.nat, N.nat_elim)
    check(0, EmptyEnvironment(), make_empty_type_env(), p, values.Top())


def test_nat_add_one():

    motive = Lambda(EmptyPattern(), Variable("nat"))

    add_one = Definition(
        VariablePattern("add_one"),
        build_arrow_type(Variable("nat"), Variable("nat")),
        #
        Lambda(VariablePattern("n"), Constructor("succ", Variable("n"))),
    )

    expect_one = Definition(
        VariablePattern("expect_one"),
        Variable("nat"),
        #
        apply(Variable("add_one"), Constructor("zero", Star())),
    )

    p = build_program(N.nat, N.nat_elim, add_one, expect_one)
    env, type_env = check(0, EmptyEnvironment(), make_empty_type_env(), p, values.Top())

    assert env["expect_one"] == values.Constructor(
        "succ", values.Constructor("zero", values.Star())
    )


def test_nat_add_one_with_elim():

    motive = Lambda(EmptyPattern(), Variable("nat"))
    
    zero_case = Constructor("succ", Constructor("zero", Star()))
    induction = lam(
        VariablePattern("n"),
        VariablePattern("Cn"),
        binder = Constructor("succ", Variable("n"))
    )

    add_one = Definition(
        VariablePattern("add_one"),
        build_arrow_type(Variable("nat"), Variable("nat")),
        #
        apply(
            Variable("nat_elim"), 
            #
            motive, 
            zero_case,
            induction,
        )
    )

    expect_one = Definition(
        VariablePattern("expect_one"),
        Variable("nat"),
        #
        apply(Variable("add_one"), Constructor("zero", Star())),
    )

    p = build_program(N.nat, N.nat_elim, add_one, expect_one)
    env, type_env = check(0, EmptyEnvironment(), make_empty_type_env(), p, values.Top())

    assert env["expect_one"] == values.Constructor(
        "succ", values.Constructor("zero", values.Star())
    )
