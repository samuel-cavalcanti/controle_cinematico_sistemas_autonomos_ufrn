from .robot_state import RobotState
from ..grid import OccupancyGrid
from .inverse_sensor_model import UltrasonicInverseModel, Space
from .inverse_sensor_model.sensor_state import SensorState


class OccupancyGridMapping:

    __occupancy_grid: OccupancyGrid
    __ultrasonics: list[UltrasonicInverseModel]

    def __init__(self, occupancy_grid: OccupancyGrid, ultrasonics: list[UltrasonicInverseModel]) -> None:
        self.__occupancy_grid = occupancy_grid
        self.__ultrasonics = ultrasonics

    def one_it(self, robot_state: RobotState):

        assert len(robot_state.normalized_distances) == len(self.__ultrasonics),\
            "O número de leituras de sensores deve ser igual ao número de sensores"

        limits = self.__occupancy_grid.limits()

        grid_width_x = int(round((limits.x_max - limits.x_min) / limits.resolution))
        grid_width_y = int(round((limits.y_max - limits.y_min) / limits.resolution))

        for x_index in range(grid_width_x-1):
            for y_index in range(grid_width_y-1):
                x_1 = x_index*limits.resolution
                y_1 = y_index*limits.resolution

                x_2 = (x_index+1)*limits.resolution
                y_2 = (y_index+1)*limits.resolution

                center_grid_cell_in_meters = (x_1 + x_2)/2, (y_1 + y_2)/2

                log_odd = self.calculate_log_odd(center_grid_cell_in_meters, robot_state)
                self.__occupancy_grid.set_log_odd(x_index, y_index, log_odd)

    def calculate_log_odd(self, center_grid_cell: tuple[float, float], robot_state: RobotState) -> float:

        log_odd = 0

        for model, distance in zip(self.__ultrasonics, robot_state.normalized_distances):
            state = SensorState(robot_state.robot_pos, distance)

            space = model.inverse_model(grid_center=center_grid_cell, sensor_state=state)

            match space:
                case Space.free:
                    log_odd += 0.05

                case Space.occupied:
                    log_odd -= 0.05

        return log_odd
