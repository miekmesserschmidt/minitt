

from dataclasses import dataclass
from typing import TypeAlias

Name : TypeAlias = str

@dataclass
class Pattern:
    pass

@dataclass
class EmptyPattern(Pattern):
    pass

@dataclass
class PairPattern(Pattern):
    a : Pattern
    b : Pattern
    
@dataclass
class VariablePattern(Pattern):
    name : Name
