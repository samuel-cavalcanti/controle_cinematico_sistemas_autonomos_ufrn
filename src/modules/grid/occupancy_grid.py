from .grid_limits import GridLimits
import numpy as np


class OccupancyGrid:
    """Grade de probabilidades se determinada área está ocupada"""

    __limits: GridLimits
    __grid: np.ndarray

    def __init__(self, limits: GridLimits) -> None:
        self.__limits = limits
        self.__grid = self.__make_grid(limits)

    def limits(self) -> GridLimits:
        return self.__limits

    def get(self, x: int, y: int) -> np.ndarray:
        """Recupera a probabilidade da célula está não ocupada"""

        return self.__grid[x, y]

    def is_valid_index(self, x: int, y: int) -> bool:

        if x < 0 or y < 0:
            return False

        try:
            self.get(x, y)
            return True

        except IndexError:
            return False

    def __make_grid(self, limits: GridLimits) -> np.ndarray:

        grid_width_x = int(round((limits.x_max - limits.x_min) / limits.resolution))
        grid_width_y = int(round((limits.y_max - limits.y_min) / limits.resolution))

        grid_points = list()

        for _ in range(grid_width_x):
            for _ in range(grid_width_y):
                grid_points.append(0)

        grid_points = np.array(grid_points)

        return grid_points.reshape((grid_width_x, grid_width_y, -1))
