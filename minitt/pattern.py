from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol


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


@dataclass
class VariablePattern(Pattern):
    name: Name

    def __contains__(self, name: Name):
        return name == self.name

    def project(self, name: Name, in_: "Value") -> "Value":
        if self.name == name:
            return in_
        else:
            raise Critical("projection error")
