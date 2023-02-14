


from minitt.errors import Critical

from minitt.expressions import Application, Expression, Lambda, Program, Star 
from minitt.declarations import Declaration
from minitt.pattern import EmptyPattern, Pattern, VariablePattern


def build_program(*declarations : Declaration) -> Expression:    
    if len(declarations) == 0:
        return Star()
    else:
        return Program(declarations[0], build_program(*declarations[1:]))
    
def apply(fn: Expression, *arguments: Expression)-> Expression:
    if len(arguments) == 0:
        raise Critical("no arguments")
    
    elif len(arguments) == 1:
        return Application(fn, arguments[0])
    
    else:
        return apply(
            Application(fn, arguments[0]), *arguments[1:]
        )
        
def lam(*var_patterns:Pattern, binder : Expression ) -> Expression:
    if len(var_patterns) == 0:
        return Lambda(EmptyPattern(), binder)
    if len(var_patterns) == 1:
        return Lambda(var_patterns[0], binder )
    else:
        return Lambda(var_patterns[0], lam(*var_patterns[1:], binder=binder) )
    
    
                
        