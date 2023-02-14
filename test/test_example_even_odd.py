from minitt.environment import EmptyEnvironment
from minitt.checking import check
from minitt.evaluate import evaluate
from minitt.expressions import (
    Application,
    Pair,
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
    build_independent_product_type,
)

from minitt.pattern import EmptyPattern, PairPattern, VariablePattern
from minitt.declarations import Definition, RecursiveDefinition

from minitt import values
from minitt.type_env import make_empty_type_env

from lib.helpers import apply, build_program, lam
import lib.nat as N
import lib.bool as B

is_even = Function(
    (
        Branch("zero", lam(binder=B.true)),
        Branch(
            "succ",
            lam(
                VariablePattern("m"), binder=apply(Variable("is_odd"), Variable("m"))  #
            ),
        ),
    )
)

is_odd = Function(
    (
        Branch("zero", lam(binder=B.false)),
        Branch(
            "succ",
            lam(
                VariablePattern("m"),
                binder=apply(Variable("is_even"), Variable("m")),
            ),
        ),
    )
)


even_odd = RecursiveDefinition(
    pattern=PairPattern(VariablePattern("is_even"), VariablePattern("is_odd")),
    of_type=build_independent_product_type(
        build_arrow_type(Variable("nat"), Variable("bool")),
        build_arrow_type(Variable("nat"), Variable("bool")),
    ),
    assignment=Pair(is_even, is_odd),
)


def test_even_odd_type_check():

    p = build_program(N.nat, B.bool_, even_odd)
    check(0, EmptyEnvironment(), {}, p, values.Top())


