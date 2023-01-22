from typing import TYPE_CHECKING, NamedTuple, Tuple, TypeAlias

from .errors import Critical


if TYPE_CHECKING:
    from .expressions import Expression
    from .environment import Environment, NormalEnvironment
    from .expressions import Branch


Name: TypeAlias = str
DeBruijnIndex: TypeAlias = int
DeBruijnLevel: TypeAlias = int
#Branches: Tuple["Branch"]
# BranchClosure: TypeAlias = Tuple[Tuple["Branch"], "Environment"]


def lookup(name:Name, branches:Tuple["Branch"]):
    for br in branches:
        if name == br.name:
            return br.expr
    else: 
        raise Critical(f"{name} not in {branches}")

class BranchClosure(NamedTuple):
    branches : Tuple["Branch", ...]
    env: "Environment"
    
    def __getitem__(self, name:Name)->"Expression":
        for br in self.branches:
            if br.name == name:
                return br.expr
        else:
            raise Critical(f"branch '{name}' not found") 
        
class NormalBranchClosure(NamedTuple):
    branches : Tuple["Branch", ...]
    env: "NormalEnvironment"
    
    def __getitem__(self, name:Name)->"Expression":
        for br in self.branches:
            if br.name == name:
                return br.expr
        else:
            raise Critical(f"branch '{name}' not found") 