from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from .node import Node
import heapq

@dataclass
class HeapItem:
    node: Node
    distance: float

    def __lt__(self, other: HeapItem):
        return self.distance < other.distance

    def __le__(self, other: HeapItem):
        return self.distance <= other.distance


class MinHeap:
    __list:list[HeapItem]

    def __init__(self) -> None:
        self.__list = list()

    def push(self, node: Node,distance:float):
        heapq.heappush(self.__list, HeapItem(node=node, distance=distance))

    def pop(self) -> Optional[Node]:
        try:
            item = heapq.heappop(self.__list)
            return item.node
        except IndexError:
          return None

    def is_not_empty(self)->bool:
        return len(self.__list) != 0
