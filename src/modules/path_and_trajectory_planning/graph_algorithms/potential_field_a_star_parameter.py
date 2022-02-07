from .a_star_search import Node
from ..potential_field.potential_field_calculator import PotentialFieldCalculator
from ...grid import GridLimits
from  .mesh_grid_graph import MeshNode
import numpy as np

class PotencialFieldAStarParameter:
    __grid_limits: GridLimits
    __field_calculator: PotentialFieldCalculator

    def __init__(self, field_calculator: PotentialFieldCalculator, limits: GridLimits) -> None:
        self.__field_calculator = field_calculator
        self.__grid_limits = limits

    def get_real_cost(self, origin: Node, target: Node) -> float:
        target_pos = self.__node_to_position(target)
        origin_pos = self.__node_to_position(origin)

        return np.abs(self.__field_calculator.calculate_potencial_value(target_pos) - self.__field_calculator.calculate_potencial_value(origin_pos))

    def get_heuristic_cost(self, origin: Node, target: Node) -> float:
        node: MeshNode = target

       
        return  0


    def __node_to_position(self,node:MeshNode)->np.ndarray:
        position_x = node.x_index * self.__grid_limits.resolution + self.__grid_limits.x_min
        position_y = node.y_index * self.__grid_limits.resolution + self.__grid_limits.x_min
        return np.array([position_x,position_y])