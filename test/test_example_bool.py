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
    One,
    Pi,
    Program,
    Set,
    Sum,
    Unit,
    Variable,
)

from minitt.pattern import EmptyPattern, VariablePattern
from minitt.declarations import Definition

from minitt import values
from minitt.type_env import make_empty_type_env


bool_ = Definition(
    pattern=VariablePattern("bool"),
    of_type=Set(),
    assignment=Sum((Branch("true", One()), Branch("false", One()))),
)

bool_elim = Definition(
    pattern=VariablePattern("bool_elim"),
    of_type=Pi(
        pattern=VariablePattern("C"),
        base=ArrowType(Variable("bool"), Set()),
        family=ArrowType(
            Application(Variable("C"), Constructor("true", Unit())),
            ArrowType(
                Application(Variable("C"), Constructor("false", Unit())),
                Pi(
                    VariablePattern("b"),
                    Variable("bool"),
                    Application(Variable("C"), Variable("b")),
                ),
            ),
        ),
    ),
    assignment=Lambda(
        VariablePattern("C"),
        Lambda(
            VariablePattern("true_case"),
            Lambda(
                VariablePattern("false_case"),
                binder=Function(
                    (
                        Branch("true", Lambda(EmptyPattern(), Variable("true_case"))),
                        Branch("false", Lambda(EmptyPattern(), Variable("false_case"))),
                    )
                ),
            ),
        ),
    ),
)


def test_bool():

    p = Program(bool_, Unit())
    check(0, EmptyEnvironment(), make_empty_type_env(), p, values.One())


def test_bool_elim():

    p = Program(bool_, Program(bool_elim, Unit()))
    check(0, EmptyEnvironment(), make_empty_type_env(), p, values.One())


def test_not():

    true_ = Constructor("true", Unit())
    false_ = Constructor("false", Unit())

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
            Program(not_, Program(not_on_true, Program(not_on_false, Unit())))
            # Unit()
        ),
    )

    env, type_env = check(0, EmptyEnvironment(), make_empty_type_env(), p, values.One())

    assert env["expect_true"] == values.Constructor("true", arg=values.Unit())
    assert env["expect_false"] == values.Constructor("false", arg=values.Unit())
