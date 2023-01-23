from decimal import DecimalException
from minitt.environment import EmptyEnvironment
from minitt.checking import check
from minitt.expressions import Branch, Function, Lambda, One, Pi, Program, Set, Sum, Unit, Variable
from minitt.pattern import EmptyPattern, VariablePattern
from minitt.declarations import Definition

from minitt import values


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

    check(0, EmptyEnvironment(), [], p, values.One())


def test_bool():
    
    bool_ = Definition(
        pattern=VariablePattern("bool"),
        of_type=Set(),
        assignment= Sum((
            Branch("true", One()),
            Branch("false", One())
        ))
    )
    
    bool_elim = Definition(
        pattern = VariablePattern("bool_elim"),
        of_type= Pi(
            pattern =VariablePattern("C"),
            base=Variable("bool"),
            family=Set(),
        ),
        assignment=Lambda(
            VariablePattern("C"),
            Lambda(VariablePattern("true_case"),
                   Lambda(VariablePattern("false_case"),
                          binder=Function((
                              Branch("true", Variable("true_case")),
                              Branch("false", Variable("false_case"))
                              ))       
                          )
                   )
        )
    )
    
    p = Program(
        bool_,
        Unit()
    )
    check(0, EmptyEnvironment(), [], p, values.One())
    
    # p = Program(
    #     bool_,
    #     Program(
    #         bool_elim,
    #         Unit()
    #     )
    # )
    # check(0, EmptyEnvironment(), [], p, values.One())
    