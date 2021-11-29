from typing import Callable

import numpy as np

from path_planning import path_by_polynomials
from robots_kinematics import pioneer
from robots_kinematics.pioneer import PioneerWheelVelocity
from utils import Position, euclidean_distance


class PathFollowController:
    __angular_velocity: Callable[[float, float], float]
    __delta_x: Callable[[float], float]
    __delta_y: Callable[[float], float]
    __velocity_function: Callable[[float], float]
    __x_lambda: Callable[[float], float]
    __y_lambda: Callable[[float], float]
    __length_path: float
    __last_time: float
    __last_lambda: float

    def __init__(self, initial_pos: Position, desired_pos: Position, initial_time_in_seconds: float, max_time: float):

        x_coefficients, y_coefficients = path_by_polynomials.find_coefficients(initial_pos, desired_pos)

        def dx(lam: float) -> float:
            return x_coefficients[1] + 2 * x_coefficients[2] * lam + 3 * x_coefficients[3] * lam ** 2

        def dy(lam: float) -> float:
            return y_coefficients[1] + 2 * y_coefficients[2] * lam + 3 * y_coefficients[3] * lam ** 2

        self.__delta_x = dx
        self.__delta_y = dy
        self.__x_lambda, self.__y_lambda, _ = path_by_polynomials.create_path_functions(x_coefficients, y_coefficients)

        self.__length_path = euclidean_distance(desired_pos.x - initial_pos.x, desired_pos.y - initial_pos.y)

        self.__velocity_function = self.__create_velocity_function(self.__length_path, max_time)

        self.__angular_velocity = self.__create_angular_velocity_function(x_coefficients, y_coefficients)

        self.__last_time = initial_time_in_seconds
        self.__last_lambda = 0.0

    def __create_angular_velocity_function(self, x_coefficients: list[float], y_coefficients: list[float]) \
            -> Callable[[float, float], float]:
        def dy_2(lam: float) -> float:
            return 2 * y_coefficients[2] + 6 * y_coefficients[3] * lam

        def dx_2(lam: float) -> float:
            return 2 * x_coefficients[2] + 6 * x_coefficients[3] * lam

        def angular_velocity(t: float, lamp: float) -> float:
            a_1 = (dy_2(lamp) * self.__delta_x(lamp) - dx_2(lamp) * self.__delta_y(lamp))
            a = self.__velocity_function(t) * a_1
            b = (self.__delta_x(lamp) ** 2 + self.__delta_y(lamp) ** 2) ** (3 / 2)
            return a / b

        return angular_velocity

    def __create_velocity_function(self, length_path, max_time_in_seconds: float) -> Callable[[float], float]:
        max_velocity = 2 * length_path / max_time_in_seconds

        def velocity(time_in_seconds: float) -> float:
            return max_velocity * (1 - np.cos(2 * np.pi * time_in_seconds / max_time_in_seconds)) / 2

        return velocity

    def step(self, current_pos: Position, time_in_seconds: float) -> PioneerWheelVelocity:
        v_t = self.__velocity_function(time_in_seconds)

        def p_lambda(lambda_value: float) -> float:
            dl = np.sqrt(self.__delta_x(lambda_value) ** 2 + self.__delta_y(lambda_value) ** 2)
            dt = time_in_seconds - self.__last_time
            return v_t * dt / dl

        lambda_t = self.__last_lambda + p_lambda(self.__last_lambda)
        self.__last_lambda = lambda_t

        q = np.array([self.__delta_x(lambda_t),
                      self.__delta_y(lambda_t),
                      self.__angular_velocity(lambda_t, time_in_seconds)])

        self.__last_time = time_in_seconds

        vel = pioneer.inverse_kinematic(theta_in_rads=current_pos.theta_in_rads, velocity=q)
        print(f"lambda {lambda_t} v_t: {v_t}", f"time {time_in_seconds} q:", q, vel.left, vel.right)

        return pioneer.inverse_kinematic(theta_in_rads=current_pos.theta_in_rads, velocity=q)
