
from minitt.environment import EmptyEnvironment
from minitt.checking import check
from minitt.expressions import Application, ArrowType, ArrowType, Branch, Constructor, Function, Lambda, One, Pi, Program, Set, Sum, Unit, Variable
from minitt.pattern import EmptyPattern, VariablePattern
from minitt.declarations import Definition

from minitt import values
from minitt.type_env import make_empty_type_env


def test_id():
    id_ = Definition(
        pattern=VariablePattern("id"),
        of_type=Pi(
            VariablePattern("A"),
            Set(),
            Pi(
                EmptyPattern(),
                Variable("A"),
                Variable("A"),
            ),
        ),
        assignment=Lambda(
            VariablePattern("A"), Lambda(VariablePattern("x"), Variable("x"))
        ),
    )

    p = Program(id_, Unit())

    check(0, EmptyEnvironment(), make_empty_type_env(), p, values.One())

