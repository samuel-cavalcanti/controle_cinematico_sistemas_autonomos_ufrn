from .grid_limits import GridLimits

from ..a_star_search import Graph

from .mesh_grid_graph import MeshGridGraph

import numpy as np

class MeshGridGraphBuild:

    __limits: GridLimits

    def __init__(self, limits: GridLimits) -> None:

        self.__limits = limits

    def build(self) -> Graph:
        grid = self.__make_grid()

        return MeshGridGraph(grid)
        
    

    def __make_grid(self) -> np.ndarray:
        x_space = np.linspace(self.__limits.x_limits[0], self.__limits.x_limits[1], 50)
        y_space = np.linspace(self.__limits.y_limits[0], self.__limits.y_limits[1], 50)

        xx, yy= np.meshgrid(x_space, y_space)

        grid_points= list()

        for x, y in zip(xx, yy):
            for x_value, y_value in zip(x, y):

                grid_points.append([x_value, y_value])

        grid_points= np.array(grid_points)

        return grid_points.reshape((len(x_space), len(y_space), -1))