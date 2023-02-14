from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, Tuple


from .errors import Critical
from .helpers import Name

if TYPE_CHECKING:
    from .values import Value


class Pattern(Protocol):
    def __contains__(self, name: Name) -> bool:
        ...

    def project(self, name: Name, in_: "Value") -> "Value":
        ...


@dataclass
class EmptyPattern(Pattern):
    def __contains__(self, name: Name) -> bool:
        return False

    def project(self, name: Name, in_: "Value") -> "Value":
        raise Critical(f"{self} is empty. Does not contain {name}")


@dataclass
class PairPattern(Pattern):
    a: Pattern
    b: Pattern

    def __contains__(self, name: Name) -> bool:
        return (name in self.a) or (name in self.b)

    def project(self, name: Name, in_: "Value") -> "Value":
        from .evaluate import first, second

        if name in self.a:
            return self.a.project(name, first(in_))
        elif name in self.b:
            return self.b.project(name, second(in_))
        else:
            raise Critical("projection error")
                
        
# @dataclass
# class MultiPattern(Pattern):
#     patterns : Tuple[Pattern,...]
    
    
#     def __contains__(self, name: Name) -> bool:
#         return any( name in p for p in self.patterns)
    
#     def first(self):
#         return self.patterns[0]
    
#     def rest(self) -> "MultiPattern":
#         _, *rest = self.patterns
#         return MultiPattern(tuple(rest))
    
#     def project(self, name: Name, in_: "Value") -> "Value":
#         from .evaluate import first, second

#         match self.patterns:
#             case (a, *_) if name in a:
#                 return a.project(name, first(in_))
#             case (_, *rest) if name in (rest_mult_p := MultiPattern(tuple(rest))):
#                 return rest_mult_p.project(name, second(in_))
#             case tuple():
#                 raise Critical(f"{self} is empty. Does not contain {name}")
#             case _:
#                 raise Critical("projection error")
                

@dataclass
class VariablePattern(Pattern):
    name: Name

    def __contains__(self, name: Name):
        return name == self.name

    def project(self, name: Name, val: "Value") -> "Value":
        if name in self:
            return val
        else:
            raise Critical("projection error")


# def build_pattern(*patterns:Pattern) -> Pattern:
#     if len(patterns) == 0:
#         return EmptyPattern()
#     elif len(patterns) == 1:
#         return patterns[0]
#     else: 
#         return MultiPattern(patterns) 
