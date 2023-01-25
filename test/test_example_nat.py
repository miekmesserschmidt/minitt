from minitt.environment import EmptyEnvironment
from minitt.checking import check
from minitt.evaluate import evaluate
from minitt.expressions import (
    Application,
    ArrowType,
    ArrowType,
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

from .helpers import apply, build_program, lam


nat = RecursiveDefinition(
    pattern=VariablePattern("nat"),
    of_type=Set(),
    assignment=Sum((Branch("zero", Top()), Branch("succ", Variable("nat")))),
)

nat_elim = RecursiveDefinition(
    pattern=VariablePattern("nat_elim"),
    of_type=Pi(
        pattern=VariablePattern("C"),
        base=ArrowType(Variable("nat"), Set()),
        family=ArrowType(
            Application(
                Variable("C"), Constructor("zero", Star())
            ),  # type of zero case
            ArrowType(
                Pi(
                    VariablePattern("n"),
                    Variable("nat"),
                    ArrowType(
                        Application(Variable("C"), Variable("n")),
                        Application(Variable("C"), Constructor("succ", Variable("n"))),
                    ),
                ),
                Pi(
                    VariablePattern("m"),
                    Variable("nat"),
                    Application(Variable("C"), Variable("m")),
                ),
            ),
        ),
    ),
    assignment=lam(
        VariablePattern("C"),
        VariablePattern("zero_case"),
        VariablePattern("g"),
        #
        binder=Function(
            (
                Branch("zero", Lambda(EmptyPattern(), Variable("zero_case"))),
                Branch(
                    "succ",
                    Lambda(
                        VariablePattern("n1"),  # argument to succ
                        apply(
                            apply(Variable("g"), Variable("n1")),
                            apply(
                                Variable("nat_elim"),
                                #
                                Variable("C"),
                                Variable("zero_case"),
                                Variable("g"),
                                Variable("n1"),
                            ),
                        ),
                    ),
                ),
            )
        ),
    ),
)


def test_nat():

    p = build_program(nat)
    check(0, EmptyEnvironment(), make_empty_type_env(), p, values.Top())


def test_nat_elim():

    p = build_program(nat, nat_elim)
    check(0, EmptyEnvironment(), make_empty_type_env(), p, values.Top())


def test_nat_add_one():

    motive = Lambda(EmptyPattern(), Variable("nat"))

    add_one = Definition(
        VariablePattern("add_one"),
        ArrowType(Variable("nat"), Variable("nat")),
        #
        Lambda(VariablePattern("n"), Constructor("succ", Variable("n"))),
    )

    expect_one = Definition(
        VariablePattern("expect_one"),
        Variable("nat"),
        #
        apply(Variable("add_one"), Constructor("zero", Star())),
    )

    p = build_program(nat, nat_elim, add_one, expect_one)
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
        ArrowType(Variable("nat"), Variable("nat")),
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

    p = build_program(nat, nat_elim, add_one, expect_one)
    env, type_env = check(0, EmptyEnvironment(), make_empty_type_env(), p, values.Top())

    assert env["expect_one"] == values.Constructor(
        "succ", values.Constructor("zero", values.Star())
    )
