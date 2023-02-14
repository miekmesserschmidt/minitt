from dataclasses import dataclass
from typing import List, NamedTuple, Tuple

from .errors import Critical

from .declarations import Declaration
from .pattern import EmptyPattern, Pattern
from .helpers import Name


@dataclass
class Expression:
    pass


@dataclass
class Variable(Expression):
    name: Name


class Branch(NamedTuple):
    name: Name
    expr: Expression


@dataclass
class Lambda(Expression):
    pattern: Pattern
    binder: Expression


@dataclass
class Application(Expression):
    fn: Expression
    argument: Expression


@dataclass
class Pi(Expression):
    pattern: Pattern
    base: Expression
    family: Expression
    
def build_arrow_type(base: Expression, output_type:Expression) -> Pi:
    return Pi(EmptyPattern(), base, output_type)

def build_multi_arrow_type(*args: Expression) -> Pi:
    if  len(args) in (0,1):
        raise Critical("attempting to build multi arrow with one or no argument")
        
    match args:
        case (base0, base1):
            return build_arrow_type(base0, base1)
        
        case (base0, *rest):
            return build_arrow_type(base0, build_multi_arrow_type(*rest))        
            
        case _:
            raise Critical("Multi arrow construction error")        


@dataclass
class Sigma(Expression):
    pattern: Pattern
    base: Expression
    family: Expression
    
def build_independent_product_type(*args: Expression) -> Sigma:
    if  len(args) in (0,1):
        raise Critical("attempting to build multi arrow with one or no argument")
    
    match args:        
        case (a,b):
            return Sigma(EmptyPattern(), a,b)

        case (a, *rest):
            return Sigma(EmptyPattern(), a, build_independent_product_type(*rest))
            
        case _:
            raise Critical("Independent product construction error")        


@dataclass
class Pair(Expression):
    a: Expression
    b: Expression


@dataclass
class Constructor(Expression):
    name: Name
    expr: Expression


@dataclass
class Sum(Expression):
    branches: Tuple[Branch, ...]


@dataclass
class Function(Expression):
    branches: Tuple[Branch, ...]


@dataclass
class First(Expression):
    of: Expression


@dataclass
class Second(Expression):
    of: Expression


@dataclass
class Program(Expression):  # EDecl
    declaration: Declaration
    next_expression: Expression


@dataclass
class Set(Expression):
    pass


@dataclass
class Top(Expression): #One  
    pass


@dataclass
class Star(Expression): #Unit
    pass


@dataclass
class Void(Expression):
    pass
