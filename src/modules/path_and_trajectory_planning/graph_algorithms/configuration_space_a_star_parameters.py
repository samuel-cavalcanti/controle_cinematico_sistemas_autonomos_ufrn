from typing import Optional
from .mesh_grid_graph import MeshNode
from .a_star_search import Node

from ...grid import Grid
import numpy as np


class ConfigurationSpaceAStarParameters:
    __goal_node: Optional[MeshNode]
    __grid: Grid

    def __init__(self, grid: Grid) -> None:
        self.__grid = grid
        self.__goal_node = None

    def set_goal(self, node: MeshNode):
        self.__goal_node = node

    def get_real_cost(self, origin: Node, target: Node) -> float:
        origin_mesh_node: MeshNode = origin
        target_mesh_node: MeshNode = target
        pos_origin = self.__grid.get(x=origin_mesh_node.x_index, y=origin_mesh_node.y_index)
        pos_target = self.__grid.get(x=target_mesh_node.x_index, y=target_mesh_node.y_index)

        return np.linalg.norm(pos_origin - pos_target)

    def get_heuristic_cost(self, origin: Node, target: Node) -> float:

        if self.__goal_node is None:
            return 0.0

        return self.get_real_cost(target, self.__goal_node)
