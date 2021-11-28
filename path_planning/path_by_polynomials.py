from typing import Callable

import numpy as np

from utils import Position, deg2rad

DELTA = deg2rad(2)


def is_in_undefined_region(angle_in_degree: float) -> bool:
    return np.pi/2 - DELTA <= angle_in_degree <= np.pi/2 + DELTA


def find_coefficients(initial_position: Position, final_position: Position) -> tuple[list[float], list[float]]:
    delta_x = final_position.x - initial_position.x
    delta_y = final_position.y - initial_position.y
    d_i = np.tan(initial_position.theta_in_rads)
    d_f = np.tan(final_position.theta_in_rads)

    final_angle_is_problematic = is_in_undefined_region(final_position.theta_in_rads)
    initial_angle_is_problematic = is_in_undefined_region(initial_position.theta_in_rads)

    if initial_angle_is_problematic and final_angle_is_problematic:
        a_0 = initial_position.x
        a_1 = 0
        a_2 = 3 * delta_x
        a_3 = -2 * delta_x

        b_0 = initial_position.y
        b_1 = delta_y
        b_2 = 0
        b_3 = delta_y - b_1 - b_2

    elif initial_angle_is_problematic:
        a_0 = initial_position.x
        a_1 = 0
        a_2 = 3 * delta_x / 2  # a_2 = delta_x - a_3, faça as contas.
        a_3 = -delta_x / 2

        b_0 = initial_position.y
        b_1 = 2 * (delta_y - d_f * delta_x) - d_f * a_3  # + B_3, mas B_3 é zero
        b_2 = 2 * d_f * delta_x - delta_y + d_f * a_3  # -2*B_3, mas B_3 é zero
        b_3 = 0
    elif final_angle_is_problematic:
        a_0 = initial_position.x
        a_1 = 3 * delta_x / 2
        a_2 = 3 * delta_x - 2 * a_1
        a_3 = a_1 - 2 * delta_x

        b_0 = initial_position.y
        b_1 = d_i * a_1
        b_2 = -delta_y
        b_3 = delta_y - d_i * a_1 - b_2

    else:
        a_0 = initial_position.x
        a_1 = delta_x
        a_2 = 0
        a_3 = delta_x - a_2 - a_1

        b_0 = initial_position.y
        b_1 = d_i * a_1
        b_2 = 3 * delta_y - 3 * d_f * delta_x + d_f * a_2 - 2 * (d_i - d_f) * a_1
        b_3 = 3 * d_f * delta_x - 2 * delta_y - d_f * a_2 - (2 * d_f - d_i) * a_1

    return [a_0, a_1, a_2, a_3], [b_0, b_1, b_2, b_3]


def create_path_functions(x_coefficients: list[float], y_coefficients: list[float]) -> \
        tuple[Callable, Callable, Callable]:
    def polynomial_function(a, b, c, d):
        return lambda x: a + b * x + c * x ** 2 + d * x ** 3

    def theta(t):
        d_y = y_coefficients[1] + 2 * y_coefficients[2] * t + 3 * x_coefficients[3] * t ** 2
        d_x = x_coefficients[1] + 2 * x_coefficients[2] * t + 3 * x_coefficients[3] * t ** 2
        return np.arctan(d_y / d_x)

    x_function = polynomial_function(x_coefficients[0], x_coefficients[1], x_coefficients[2], x_coefficients[3])
    y_function = polynomial_function(y_coefficients[0], y_coefficients[1], y_coefficients[2], y_coefficients[3])

    return x_function, y_function, theta


def path_creator(initial_position: Position, final_position: Position) -> tuple[Callable, Callable, Callable]:
    x_coefficients, y_coefficients = find_coefficients(initial_position, final_position)
    p_x, p_y, theta_t = create_path_functions(x_coefficients, y_coefficients)
    return p_x, p_y, theta_t


def path_points_generator(p_x, p_y) -> list[float]:
    lamb = np.arange(0.0, 1.0, 0.001)
    positions = []
    for value in lamb:
        positions += [p_x(value), p_y(value), 0.05]

    return positions
