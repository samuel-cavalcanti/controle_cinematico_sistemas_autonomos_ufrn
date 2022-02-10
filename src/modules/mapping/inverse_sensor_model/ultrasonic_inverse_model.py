

from ...utils import Position
import numpy as np
from .space import Space
from ..robot_state import RobotState

from .ultrasonic_internal_parameters import UltrasonicInternalParameters




GridCenter = tuple[float, float]


class UltrasonicInverseModel:

    __position_relative_to_robot: Position
    __internal_parameters: UltrasonicInternalParameters

    def __init__(self, ultrasonic_position: Position, parameters: UltrasonicInternalParameters) -> None:
        self.__position_relative_to_robot = ultrasonic_position
        self.__internal_parameters = parameters

    def inverse_model(self, robot_state: RobotState, grid_center: GridCenter) -> Space:

        sensor_position = self.__get_current_sensor_position(robot_state.robot_position)

        r, phi = self.__translate_to_sensor_and_covert_to_polar_system(sensor_position, grid_center)

        distance_in_meters = robot_state.normalized_distance*self.__internal_parameters.max_distance_in_meters

        is_angle_in_range = np.abs(phi) < self.__internal_parameters.alpha_in_rads/2.0

        is_ray_in_range = self.__internal_parameters.min_distance_in_meters < r < self.__internal_parameters.max_distance_in_meters

        is_in_free_space = r <= distance_in_meters

        if is_angle_in_range and is_ray_in_range:

            if is_in_free_space:
                return Space.free
            else:
                return Space.occupied

        else:
            return Space.out_of_range

    def __get_current_sensor_position(self, robot_position: Position) -> Position:

        x = robot_position.x + self.__position_relative_to_robot.x
        y = robot_position.y + self.__position_relative_to_robot.y
        theta = robot_position.theta_in_rads + self.__position_relative_to_robot.theta_in_rads

        return Position(x, y, theta)

    @staticmethod
    def __translate_to_sensor_and_covert_to_polar_system(sensor_pos: Position, grid_center: GridCenter) -> tuple[float, float]:
        delta_x = grid_center[0] - sensor_pos.x
        delta_y = grid_center[1] - sensor_pos.y

        r = np.hypot(delta_x, delta_y)
        phi = np.arctan2(delta_y, delta_x) - sensor_pos.theta_in_rads

        return r, phi
