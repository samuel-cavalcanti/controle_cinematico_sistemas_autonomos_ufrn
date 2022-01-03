from __future__ import annotations
from dataclasses import dataclass


@dataclass
class DictNode:
    name: str
 

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, __o: DictNode) -> bool:
        '''a == b, equivale  a.__eq__(b)'''
        return self.name == __o.name
