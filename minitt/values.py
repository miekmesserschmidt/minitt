

from dataclasses import dataclass
from typing import Tuple
from .expressions import Branch
from .environment import Environment

from .helpers import BranchClosure, DeBruijnIndex, Name

from .closure import ClosureBase


class Value:
    pass

@dataclass
class Lambda(Value):
    closure : ClosureBase
    
@dataclass
class Pair(Value):
    a : Value
    b : Value
    
@dataclass
class Constructor(Value):
    name : Name
    arg : Value
    
    def __post_init__(self):
        print(f"=>>>>>>{self=}")
        

@dataclass
class Pi(Value):
    base : Value
    fam : ClosureBase


@dataclass
class Sigma(Value):
    base : Value
    fam : ClosureBase



@dataclass
class Function(Value):
    branch_closure : BranchClosure #SClos

@dataclass
class Sum(Value):
    branch_closure : BranchClosure #SClos


@dataclass
class Unit(Value):
    pass

@dataclass
class One(Value):
    pass


@dataclass
class Set(Value):
    pass

@dataclass
class NeutralValue(Value):
    neutral: "Neutral"




#########3
class Neutral:
    pass


@dataclass
class Variable(Neutral):
    index : DeBruijnIndex
    
@dataclass
class Application(Neutral):
    fn : Neutral
    arg : Value
    
@dataclass
class First(Neutral):
    of : Neutral
    
@dataclass
class Second(Neutral):
    of : Neutral

@dataclass
class NeutralFunction(Neutral):
    branch_closure : BranchClosure
    scrutinee : Neutral
    
