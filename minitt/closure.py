from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol





from .helpers import Name



if TYPE_CHECKING:
    from .values import Value
    from .expressions import Expression
    from .pattern import Pattern
    from .environment import Environment
    
class ClosureBase(Protocol):
    
    def instantiate(self, v: "Value")->"Value":
        ...


@dataclass
class Closure(ClosureBase):
    pattern: "Pattern"
    expr: "Expression"
    environment: "Environment"
    
    def instantiate(self, v: "Value") -> "Value":
        from .evaluate import evaluate
        from .environment import UpVar
        extended_env = UpVar(self.environment, self.pattern, v)
        return evaluate(self.expr, extended_env)


@dataclass
class ClosureComposition(ClosureBase):
    cl: ClosureBase
    name: Name

    def instantiate(self, v: "Value") -> "Value":
        from .values import Constructor        
        print(f"{v=}")
        return self.cl.instantiate(Constructor(self.name, v))
