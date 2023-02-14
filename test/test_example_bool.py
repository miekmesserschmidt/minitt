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
from minitt.declarations import Definition

from minitt import values
from minitt.type_env import make_empty_type_env


from lib.bool import bool_, bool_elim

def test_bool():

    p = Program(bool_, Star())
    check(0, EmptyEnvironment(), make_empty_type_env(), p, values.Top())


def test_bool_elim():

    p = Program(bool_, Program(bool_elim, Star()))
    check(0, EmptyEnvironment(), make_empty_type_env(), p, values.Top())


def test_not():

    true_ = Constructor("true", Star())
    false_ = Constructor("false", Star())

    motive = Lambda(EmptyPattern(), Variable("bool"))

    not_ = Definition(
        VariablePattern("not"),
        Pi(VariablePattern("b"), Variable("bool"), Variable("bool")),
        Application(
            Application(Application(Variable("bool_elim"), motive), false_), true_
        ),
    )

    not_on_true = Definition(
        VariablePattern("expect_false"),
        Variable("bool"),
        Application(Variable("not"), true_),
    )
    not_on_false = Definition(
        VariablePattern("expect_true"),
        Variable("bool"),
        Application(Variable("not"), false_),
    )

    p = Program(
        bool_,
        Program(
            bool_elim,
            Program(not_, Program(not_on_true, Program(not_on_false, Star())))
            # Unit()
        ),
    )

    env, type_env = check(0, EmptyEnvironment(), make_empty_type_env(), p, values.Top())

    assert env["expect_true"] == values.Constructor("true", arg=values.Star())
    assert env["expect_false"] == values.Constructor("false", arg=values.Star())
