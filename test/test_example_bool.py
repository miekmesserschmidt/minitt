from decimal import DecimalException
from pydoc import ErrorDuringImport
from minitt.environment import EmptyEnvironment
from minitt.checking import check
from minitt.expressions import Application, ArrowType, ArrowType, Branch, Constructor, Function, Lambda, One, Pi, Program, Set, Sum, Unit, Variable
from minitt.pattern import EmptyPattern, VariablePattern
from minitt.declarations import Definition

from minitt import values


bool_ = Definition(
    pattern=VariablePattern("bool"),
    of_type=Set(),
    assignment= Sum((
        Branch("true", One() ),
        Branch("false", One() )
    ))
)

bool_elim = Definition(
    pattern = VariablePattern("bool_elim"),
    of_type= Pi(
        pattern =VariablePattern("C"),
        base=ArrowType(Variable("bool"), Set()),
        family= ArrowType(
            Application(Variable("C"), Constructor("true", Unit())),
            ArrowType(
                Application(Variable("C"), Constructor("false", Unit())),
                Pi(
                    VariablePattern("b"),
                    Variable("bool"),
                    Application(Variable("C"), Variable("b"))
                )
            )
        ),
    ),
    assignment=Lambda(
        VariablePattern("C"),
        Lambda(VariablePattern("true_case"),
                Lambda(VariablePattern("false_case"),
                        binder=Function((
                            Branch("true", Lambda(EmptyPattern(), Variable("true_case")) ),
                            Branch("false", Lambda(EmptyPattern(), Variable("false_case"))
                            ))       
                        )
                )
        )
    )
)



def test_bool():
    
        
    p = Program(
        bool_,
        Unit()
    )
    check(0, EmptyEnvironment(), [], p, values.One())
    

    
def test_bool_elim():
    
    
    
    p = Program(
        bool_,
        Program(
            bool_elim,
            Unit()
        )
    )
    check(0, EmptyEnvironment(), [], p, values.One())
