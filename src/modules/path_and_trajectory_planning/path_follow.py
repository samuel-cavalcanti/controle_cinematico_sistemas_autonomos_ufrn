import numpy as np

from ..utils.position import Position


class PathFollow:
    __path: np.ndarray
    __current_index: int

    def __init__(self, path: np.ndarray) -> None:
        self.__path = path
        self.__current_index = 0

    def step(self, current_position: Position) -> Position:
        """Retorna a posição desejada do robô dado a posição atual"""

        desired_point = self.__get_desired_point()

        if self.__is_arrival(current_position, desired_point):
            self.__next_point()

        return self.__point_to_position(self.__get_desired_point())

    def is_ended(self)->bool:
        return  self.__current_index + 1 >= len(self.__path)

    def __point_to_position(self, point: np.ndarray) -> Position:
        x = point[0]
        y = point[1]
        theta = np.arctan2(y, x)

        return Position(x=x, y=y, theta_in_rads=theta)

    def __get_desired_point(self) -> np.ndarray:
        return self.__path[self.__current_index]

    def __next_point(self) -> None:
        if self.is_ended():
            return

        self.__current_index += 1

    def __is_arrival(self, current: Position, desired: np.ndarray) -> bool:
        precision_in_meters = 0.1
        arrival_x = np.abs(current.x - desired[0]) <= precision_in_meters
        arrival_y = np.abs(current.y - desired[1]) <= precision_in_meters
        return arrival_x and arrival_y
