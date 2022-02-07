
from .grid_limits import GridLimits
from ..polygon_collision_detection import polygon_collision_detection
import numpy as np
from ..utils import Polygon, Vertex


class ConfigurationSpaceGrid:
    __limits: GridLimits
    __grid: np.ndarray

    def __init__(self, limits: GridLimits, c_space_obstacles: list[np.ndarray]) -> None:
        self.__limits = limits
        self.__grid = self.__make_grid(limits, c_space_obstacles)

    def limits(self) -> GridLimits:
        return self.__limits

    def get(self, x: int, y: int) -> np.ndarray:
        return self.__grid[x, y]

    def is_valid_index(self, x: int, y: int) -> bool:

        if x < 0 or y < 0:
            return False

        try:
            self.get(x, y)
            return True

        except IndexError:
            return False

    def __make_grid(self, limits: GridLimits, obstacles_in_c_space: list[np.ndarray]) -> np.ndarray:

        grid_width_x = int(round((limits.x_max - limits.x_min) / limits.resolution))
        grid_width_y = int(round((limits.y_max - limits.y_min) / limits.resolution))

        x_space = np.linspace(limits.x_min, limits.x_max, grid_width_x)
        y_space = np.linspace(limits.y_min, limits.y_max, grid_width_y)

        grid_points = list()

        for x_value in x_space:
            for y_value in y_space:
                if self.__collided_with_polygons(point=(x_value, y_value), obstacles=obstacles_in_c_space):
                    grid_points.append([float('inf'), float('inf')])
                else:
                    grid_points.append([x_value, y_value])

        grid_points = np.array(grid_points)

        print('grid_points shape: ', grid_points.shape)

        return grid_points.reshape((len(x_space), len(y_space), -1))

    def __collided_with_polygons(self, point: tuple[float, float], obstacles: list[np.ndarray]) -> bool:

        for vertices in obstacles:
            polygon = self.__numpy_to_polygon(vertices)
            if polygon_collision_detection.check_detection_between_polygon_and_point(point=point, poly=polygon):
                return True

        return False

    def __numpy_to_polygon(self, vertices: np.ndarray) -> Polygon:

        vertices = [Vertex('Test', position=vertex.tolist()) for vertex in vertices]
        return Polygon(name='Test', vertices=vertices)
