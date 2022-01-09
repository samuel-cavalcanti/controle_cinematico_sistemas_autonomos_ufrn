from ....utils.polygon import Polygon
from ....utils.grid.grid_limits import GridLimits

from ..a_star_search import Graph
from .mesh_grid_graph import MeshGridGraph

import numpy as np
from .... import polygon_collision_detection


class MeshGridGraphBuilder:

    __limits: GridLimits
    __obstacles: list[Polygon]

    def __init__(self, limits: GridLimits, obstacles: list[Polygon]) -> None:
        self.__limits = limits
        self.__obstacles = obstacles

    def build(self) -> Graph:
        grid = self.__make_grid()

        return MeshGridGraph(grid)

    def __make_grid(self) -> np.ndarray:
        x_space = np.linspace(self.__limits.x_min, self.__limits.x_max, 50)
        y_space = np.linspace(self.__limits.y_min, self.__limits.y_max, 50)

        xx, yy = np.meshgrid(x_space, y_space)

        grid_points = list()

        for x, y in zip(xx, yy):
            for x_value, y_value in zip(x, y):
                if self.__is_collided_With_obstacles(point=(x_value, y_value)):
                    grid_points.append([x_value, y_value])
                else:
                    grid_points.append([None, None])

        grid_points = np.array(grid_points)

        return grid_points.reshape((len(x_space), len(y_space), -1))

    def __is_collided_With_obstacles(self, point: tuple[float, float]) -> bool:
        for polygon in self.__obstacles:
            if polygon_collision_detection.check_detection_between_polygon_and_point(poly=polygon, point=point):
                return True
        return False
