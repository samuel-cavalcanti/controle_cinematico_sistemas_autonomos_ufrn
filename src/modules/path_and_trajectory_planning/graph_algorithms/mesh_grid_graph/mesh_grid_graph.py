from typing import Optional
from .mesh_node import MeshNode
from ..a_star_search import Node

import numpy as np


class MeshGridGraph:

    __grid: np.ndarray
    __goal_node: Optional[MeshNode]

    def __init__(self, grid: np.ndarray) -> None:
        assert grid.shape[-1] == 2, "expected and grid with last shape is x,y pos"
        assert len(grid.shape) == 3, "expected an grid 3D shape"
        self.__grid = grid
        self.__goal_node = None

    def set_goal(self, node: MeshNode):
        self.__goal_node = node

    def get_neighbors(self, node: Node) -> list[Node]:
        mesh_node: MeshNode = node
        neighbors = list()
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                index = (mesh_node.x_index + i, mesh_node.y_index + j)
                if (i, j) == (0, 0):
                    continue
                if not self.__out_of_bounds(index):
                    value = self.__grid[index[1], index[0]]
                    if value[0] != float('inf'):
                        neighbors.append(MeshNode(x_index=index[0], y_index=index[1]))

        return neighbors

    def get_real_cost(self, origin: Node, target: Node) -> float:
        origin_mesh_node: MeshNode = origin
        target_mesh_node: MeshNode = target
        pos_origin = self.__grid[origin_mesh_node.y_index][origin_mesh_node.x_index]
        pos_target = self.__grid[target_mesh_node.y_index][target_mesh_node.x_index]

        return np.linalg.norm(pos_origin - pos_target)

    def get_heuristic_cost(self, origin: Node, target: Node) -> float:

        if self.__goal_node is None:
            return 0.0

        return self.get_real_cost(target, self.__goal_node)

    def __out_of_bounds(self, index: tuple[int, int]) -> bool:

        try:
            self.__grid[index[1], index[0]]
            return False
        except IndexError:
            return True
