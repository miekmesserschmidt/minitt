from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, Sized

from .evaluate import evaluate

from .errors import Critical


if TYPE_CHECKING:
    from .helpers import Name
    from .declarations import Declaration, Definition, RecursiveDefinition
    from .values import Value
    from .pattern import Pattern
    from .normal_forms import NormalExpression


class Environment(Sized, Protocol):
    def __getitem__(self, item: "Name") -> "Value":
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
    previous_env: "Environment"
    pattern: "Pattern"
    val: "Value"

    def __getitem__(self, name: "Name") -> "Value":
        return (
            self.pattern.project(name, self.val)
            if name in self.pattern
            else self.previous_env[name]
        )

    def __len__(self) -> int:
        return len(self.previous_env) + 1


@dataclass
class UpDeclaration(Environment):
    previous_env: "Environment"
    decl: "Declaration"

    def __getitem__(self, name: "Name") -> "Value":
        from .declarations import Definition, RecursiveDefinition

        match self.decl:

            case Definition(pattern, _, assignment) if name in pattern:
                v = evaluate(assignment, self.previous_env)
                return pattern.project(name, v)

            case RecursiveDefinition(pattern, _, assignment) if name in pattern:
                v = evaluate(assignment, self)  # uses self as environment
                return pattern.project(name, v)

            case _:
                return self.previous_env[name]

    def __len__(self) -> int:
        return len(self.previous_env) + 1


##################3


class NormalEnvironment:
    pass


@dataclass
class NormalEmptyEnvironment(NormalEnvironment):
    pass


@dataclass
class NormalUpVar(NormalEnvironment):
    previous_env: "NormalEnvironment"
    pattern: "Pattern"
    val: "NormalExpression"


@dataclass
class NormalUpDeclaration(NormalEnvironment):
    previous_env: "NormalEnvironment"
    decl: "Declaration"
