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
    build_multi_arrow_type,
)

from minitt.pattern import EmptyPattern, VariablePattern
from minitt.declarations import Definition, RecursiveDefinition

from minitt import values
from minitt.type_env import make_empty_type_env

from .helpers import apply, build_program, lam


nat = RecursiveDefinition(
    pattern=VariablePattern("nat"),
    of_type=Set(),
    assignment=Sum((Branch("zero", Top()), Branch("succ", Variable("nat")))),
)

zero = Constructor("zero", Star())
succ_of = lambda n: Constructor("succ", n)

nat_elim = RecursiveDefinition(
    pattern=VariablePattern("nat_elim"),
    of_type=Pi(
        pattern=VariablePattern("C"),
        base=build_arrow_type(Variable("nat"), Set()),
        family=build_multi_arrow_type(
            Application(Variable("C"), zero),  # type of zero case
            #
            Pi( #induction case
                pattern=VariablePattern("n"),
                base=Variable("nat"),
                family=build_arrow_type(
                    apply(Variable("C"), Variable("n")),
                    apply(Variable("C"), succ_of(Variable("n"))),
                ),
            ),
            # output
            Pi(
                VariablePattern("m"),
                Variable("nat"),
                Application(Variable("C"), Variable("m")),
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
                Branch("zero", lam(binder=Variable("zero_case"))),
                Branch(
                    "succ",
                    lam(
                        VariablePattern("n1"),  # argument to succ
                        binder=apply(
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
