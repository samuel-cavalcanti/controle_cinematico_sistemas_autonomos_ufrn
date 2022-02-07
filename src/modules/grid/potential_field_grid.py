from .grid_limits import GridLimits
from ..path_and_trajectory_planning.potential_field.potential_field_calculator import PotentialFieldCalculator
import numpy as np


class PotentialFielGrid:
    __limits: GridLimits
    __calculator: PotentialFieldCalculator
    __threshold_potencial_value = 50  # valor obitido experimentalmente

    def __init__(self, grid_limits: GridLimits, calculator: PotentialFieldCalculator) -> None:
        self.__limits = grid_limits
        self.__calculator = calculator

    def limits(self) -> GridLimits:
        return self.__limits

    def get(self, x: int, y: int) -> np.ndarray:

        position_x = x * self.__limits.resolution + self.__limits.x_min
        position_y = y * self.__limits.resolution + self.__limits.y_min

        return np.array([position_x, position_y])

    def is_valid_index(self, x: int, y: int) -> bool:

        real_pos = self.get(x, y)

        if real_pos[0] >= self.__limits.x_max or real_pos[1] >= self.__limits.y_max:
            return False

        if real_pos[0] <= self.__limits.x_min or real_pos[1] <= self.__limits.y_min:
            return False

        value = self.__calculator.calculate_potencial_value(real_pos)

        if value > self.__threshold_potencial_value:
            return False

        return True
