from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, Sized

from .evaluate import evaluate

from .errors import Critical


if TYPE_CHECKING:
    from .helpers import Name
    from .declarations import Declaration, Definition, RecursiveDefinition
    from .values import Value
    from .pattern import Pattern


class Environment(Sized, Protocol):
    def __getitem__(self, item: "Name")-> "Value":
        ...
        
    def __len__(self) -> int:
        ...


@dataclass
class EmptyEnvironment(Environment):
    def __getitem__(self, name: "Name") -> "Value":
        raise Critical(f"Empty environment. {name}")
    
    def __len__(self) -> int:
        return 0 


@dataclass
class UpVar(Environment):
    env: "Environment"
    pattern: "Pattern"
    val: "Value"

    def __getitem__(self, name: "Name")-> "Value":
        return (
            self.pattern.project(name, self.val)
            if name in self.pattern
            else self.env[name]
        )


    def __len__(self) -> int:
        return len(self.env) + 1 

@dataclass
class UpDeclaration(Environment):
    env: "Environment"
    decl: "Declaration"

    def __getitem__(self, name: "Name")-> "Value":
        match self.decl:
            case Definition(pattern, _, assignment) if name in pattern:
                return pattern.project(name, evaluate(assignment, self.env))
            case RecursiveDefinition(pattern, _, assignment) if name in pattern:
                return pattern.project(name, evaluate(assignment, self))
            case _:
                return self.env[name]

    def __len__(self) -> int:
        return len(self.env) + 1 
