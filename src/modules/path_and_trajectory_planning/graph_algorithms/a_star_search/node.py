from __future__ import annotations
from typing import Protocol


class Node(Protocol):

    def __hash__(self) -> int:
        '''Um nó tem que ser hashavel
            para que uma tabela hash consiga indexar 
        '''

    def __eq__(self, __o: Node) -> bool:
        '''a == b, equivale  a.__eq__(b)'''
