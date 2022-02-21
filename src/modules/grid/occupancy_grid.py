from .grid_limits import GridLimits
import numpy as np


class OccupancyGrid:
    """
        Grade de log-odds se determinada área está ocupada
        cada célula da matriz corresponte a um centroide do grid
    """

    __limits: GridLimits
    __grid: np.ndarray

    def __init__(self, limits: GridLimits) -> None:
        self.__limits = limits
        self.__grid = self.__make_grid(limits)

    def limits(self) -> GridLimits:
        return self.__limits

    def get(self, x: int, y: int) -> np.ndarray:
        """Recupera o log-odd da célula está não ocupada"""

        return self.__grid[x, y]

    def set_log_odd(self, x: int, y: int, value: float):
        """atualiza o log-odd da célula x,y, se o index não válido retorna um IndexError"""
        if self.is_valid_index(x, y):
            self.__grid[x, y] = value
        else:
            raise IndexError

    def get_probability_matrix(self) -> np.ndarray:
        """
            retorna uma matriz de probabilides, essa função é utilizada para criar gráficos
            de modo que seja possível visualizar a grade de ocupação, no caso a matriz se assemelha
            a uma imagem em ton de cinza.
        """
        return 1 - 1/(1 + np.exp(self.__grid))

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

        return np.zeros(shape=(grid_width_x-1, grid_width_y-1, 1))
