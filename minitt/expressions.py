from dataclasses import dataclass
from typing import List, NamedTuple, TypeAlias

from .declarations import Declaration
from .pattern import Pattern


Name: TypeAlias = str


@dataclass
class Expression:
    pass


@dataclass
class Variable(Expression):
    name: Name


class Branch(NamedTuple):
    name: Name
    value: Expression


@dataclass
class Set(Expression):
    pass


@dataclass
class One(Expression):
    pass


@dataclass
class Unit(Expression):
    pass


@dataclass
class Void(Expression):
    pass


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


@dataclass
class Sigma(Expression):
    pattern: Pattern
    base: Expression
    family: Expression


@dataclass
class Pair(Expression):
    a: Expression
    b: Expression


@dataclass
class Constructor(Expression):
    name: str
    expr: Expression


@dataclass
class Sum(Expression):
    branches: List[Branch]


@dataclass
class Function(Expression):
    branches: List[Branch]


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
