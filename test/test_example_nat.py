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
from minitt.declarations import Definition, RecursiveDefinition

from minitt import values


nat = RecursiveDefinition(
    pattern=VariablePattern("nat"),
    of_type=Set(),
    assignment=Sum((Branch("zero", One()), Branch("succ", Variable("nat")))),
)

nat_elim = RecursiveDefinition(
    pattern=VariablePattern("nat_elim"),
    of_type=Pi(
        pattern=VariablePattern("C"),
        base=ArrowType(Variable("nat"), Set()),
        family=ArrowType(
            Application(Variable("C"), Constructor("zero", Unit())),
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
    assignment=Lambda(
        VariablePattern("C"),
        Lambda(
            VariablePattern("zero_case"),
            Lambda(
                VariablePattern("g"),
                binder=Function(
                    (
                        Branch("zero", Lambda(EmptyPattern(), Variable("zero_case"))),
                        Branch(
                            "succ",
                            Lambda(
                                VariablePattern("n1"),
                                Application(
                                    Application(Variable("g"), Variable("n1")),
                                    #
                                    Application(
                                        Application(
                                            Application(
                                                Application(
                                                    Variable("nat_elim"), Variable("C")
                                                ),
                                                Variable("zero_case"),
                                            ),
                                            Variable("g"),
                                        ),
                                        Variable("n1"),
                                    ),
                                ),
                            ),
                        ),
                    )
                ),
            ),
        ),
    ),
)


def test_nat():

    p = Program(nat, Unit())
    check(0, EmptyEnvironment(), [], p, values.One())


def test_nat_elim():

    p = Program(nat, Program(nat_elim, Unit()))
    check(0, EmptyEnvironment(), [], p, values.One())
