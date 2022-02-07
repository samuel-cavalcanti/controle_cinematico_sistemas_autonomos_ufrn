import os
import sys

import numpy as np
from matplotlib import pyplot as plt

try:
    from src.modules.utils import Position, deg2rad, rad2deg
except ModuleNotFoundError:
    sys.path.append(os.getcwd())
    from src.modules.utils import Position, deg2rad, rad2deg


from src.modules.path_and_trajectory_planning import path_by_polynomials

N_DIGITS = 1


def coefficients_to_polynomial_string(coefficients: list[float]):
    return f'{round(coefficients[0], N_DIGITS)} + {round(coefficients[1], N_DIGITS)}λ + {round(coefficients[2], N_DIGITS)}λ² + {round(coefficients[3], N_DIGITS)}λ³'


def coefficients_to_derivative_polynomial(coefficients: list[float]):
    return f'{round(coefficients[1], N_DIGITS)} + {round(2 * coefficients[2], N_DIGITS)}λ  + {round(3 * coefficients[3], N_DIGITS)}λ²'


def next_figure():
    plt.figure(plt.gcf().number + 1)


def position_to_string(pos: Position):
    return f"({pos.x},{pos.y},{rad2deg(pos.theta_in_rads)})"


def plot_position(initial_pos: Position, final_pos: Position):
    x_coefficients, y_coefficients = path_by_polynomials.find_coefficients(initial_pos, final_pos)
    p_x, p_y, p_theta = path_by_polynomials.create_path_functions(x_coefficients=x_coefficients,
                                                                  y_coefficients=y_coefficients)

    polynomial_x = coefficients_to_polynomial_string(x_coefficients)
    polynomial_y = coefficients_to_polynomial_string(y_coefficients)

    lamp = np.arange(0.0, 1.0, 0.001)

    fig, ax = plt.subplots()
    fig.set_size_inches(18.5, 10.5)
    ax.plot(p_x(lamp), p_y(lamp))
    title = f'posição inicial: {position_to_string(initial_pos)} , posição final {position_to_string(final_pos)}  do robô com $\lambda$ entre [0,1] '
    ax.set(title=title)
    ax.set_xlabel('$x(\lambda) =' + polynomial_x + '$')
    ax.set_ylabel('$y(\lambda) = ' + polynomial_y + '$', rotation=0, )
    ax.yaxis.set_label_coords(-0.1, 0.5)
    ax.set_autoscale_on(True)

    ax.grid()
    ax.scatter(p_x(0.5), p_y(0.5), c='g')
    plt.draw()

    fig, ax = plt.subplots()
    fig.set_size_inches(18.5, 10.5)
    theta_values = [p_theta(l) for l in lamp]
    ax.plot(lamp, theta_values)
    ax.scatter(0.5, p_theta(0.5), c='g')
    dy_string = coefficients_to_derivative_polynomial(y_coefficients)
    dx_string = coefficients_to_derivative_polynomial(x_coefficients)
    title = '$\\theta(\lambda) = tan^{-1}( \\frac{' + dy_string + '}{ ' + dx_string + '})$ com $\lambda$ entre [0,1] '

    ax.set(title=title)
    plt.draw()


def main():
    plot_position(initial_pos=Position(0, 0, deg2rad(90)), final_pos=Position(10, 10, deg2rad(90)))

    plot_position(initial_pos=Position(0, 0, deg2rad(90)), final_pos=Position(10, 10, 0))

    initial = Position(x=-1.2945, y=0.050001, theta_in_rads=0)
    final = Position(1.9, 2.1, deg2rad(90))
    plot_position(initial_pos=initial, final_pos=final)

    plot_position(initial_pos=Position(0, 0, 0), final_pos=Position(10, 10, deg2rad(90)))

    plt.show()

    pass


if __name__ == '__main__':
    main()
