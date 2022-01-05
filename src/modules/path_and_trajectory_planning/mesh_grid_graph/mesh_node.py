from __future__ import annotations
from dataclasses import dataclass


@dataclass
class MeshNode:
    x_index: int
    y_index: int

    def __hash__(self) -> int:
        '''Um nó tem que ser hashavel
            para que uma tabela hash consiga indexar 
        '''
        return hash(f'{self.x_index}{self.y_index}')

    def __eq__(self, __o: MeshNode) -> bool:
        '''a == b, equivale  a.__eq__(b)'''
        return self.x_index == __o.x_index and self.y_index == __o.y_index
