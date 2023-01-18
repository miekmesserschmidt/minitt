from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .expressions import Expression
    from .pattern import Pattern


@dataclass
class Declaration:
    pass


@dataclass
class Definition(Declaration):
    pattern: "Pattern"
    of_type: "Expression"
    assignment: "Expression"


@dataclass
class RecursiveDefinition(Declaration):
    pattern: "Pattern"
    of_type: "Expression"
    assignment: "Expression"
