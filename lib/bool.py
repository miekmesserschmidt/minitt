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


bool_ = Definition(
    pattern=VariablePattern("bool"),
    of_type=Set(),
    assignment=Sum((Branch("true", Top()), Branch("false", Top()))),
)

true = Constructor("true", Star())
false = Constructor("false", Star())

bool_elim = Definition(
    pattern=VariablePattern("bool_elim"),
    of_type=Pi(
        pattern=VariablePattern("C"),
        base=build_arrow_type(Variable("bool"), Set()),
        family=build_arrow_type(
            Application(Variable("C"), true),
            build_arrow_type(
                Application(Variable("C"), false),
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
