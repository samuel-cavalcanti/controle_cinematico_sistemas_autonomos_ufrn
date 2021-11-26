import os
import sys
import ctypes
import time

import numpy as np
from matplotlib import pyplot as plt
from coppeliasim.sim import simxPackFloats, simxUnpackFloats, simxWriteStringStream, simx_opmode_oneshot

sys.path.append(os.getcwd())
from utils import Position, find_coefficients, create_path_functions

N_DIGITS = 2


def coefficients_to_polynomial_string(coefficients: list[float]):
    return f'{round(coefficients[0], N_DIGITS)} + {round(coefficients[1], N_DIGITS)}λ + {round(coefficients[2], N_DIGITS)}λ² + {round(coefficients[3], N_DIGITS)}λ³'


def coefficients_to_derivative_polynomial(coefficients: list[float]):
    return f'{round(coefficients[1], N_DIGITS)} + {2 * round(coefficients[2], N_DIGITS)}λ  + {3 * round(coefficients[3], N_DIGITS)}λ²'


def increment_plot():
    plt.figure(plt.gcf().number + 1)


def position_to_string(pos: Position):
    return f"({pos.x},{pos.y},{pos.theta_in_degree})"


def plot_position(initial_pos: Position, final_pos: Position):
    x_coefficients, y_coefficients = find_coefficients(initial_pos, final_pos)
    p_x, p_y, theta_t = create_path_functions(x_coefficients, y_coefficients)

    polynomial_x = coefficients_to_polynomial_string(x_coefficients)
    polynomial_y = coefficients_to_polynomial_string(y_coefficients)
    print(polynomial_x)

    print(polynomial_y)

    t = np.arange(0.0, 1.0, 0.001)

    fig, ax = plt.subplots()
    fig.set_size_inches(18.5, 10.5)
    ax.plot(p_x(t), p_y(t))
    title = f'posição inicial: {position_to_string(initial_pos)} , posição final {position_to_string(final_pos)}  do robô com $\lambda$ entre [0,1] '
    ax.set(title=title)
    ax.set_xlabel('$x(\lambda) =' + polynomial_x + '$')
    ax.set_ylabel('$y(\lambda) = ' + polynomial_y + '$', rotation=0, )
    ax.yaxis.set_label_coords(-0.1, 0.5)
    ax.set_autoscale_on(True)

    ax.grid()
    ax.scatter(p_x(0.5), p_y(0.5), c='g')
    plt.draw()
    plt.savefig(f'initial-{position_to_string(initial_pos)} final-{position_to_string(final_pos)}')

    fig, ax = plt.subplots()
    fig.set_size_inches(18.5, 10.5)
    ax.plot(t, theta_t(t))
    ax.scatter(0.5, theta_t(0.5), c='g')
    dy_string = coefficients_to_derivative_polynomial(y_coefficients)
    dx_string = coefficients_to_derivative_polynomial(x_coefficients)
    title = '$\\theta(\lambda) = tan^{-1}( \\frac{' + dy_string + '}{ ' + dx_string + '})$ com $\lambda$ entre [0,1] '
    print(title)
    ax.set(title=title)
    plt.draw()
 

 ############ ADICIONADO POR JÚLIA #########################################################
def send_path_4_drawing (path, clientID, sleep_time=0.07):
    for point in path:
        packedData = simxPackFloats(point)
        raw_bytes = (ctypes.c_ubyte * len(packedData)).from_buffer_copy(packedData)
        returnCode = simxWriteStringStream(clientID, "path_coord", packedData, simx_opmode_oneshot)
    time.sleep(sleep_time)
############################################################################################


def main():
    plot_position(initial_pos=Position(0, 0, 0), final_pos=Position(10, 10, 45))

    plot_position(initial_pos=Position(0, 0, 90), final_pos=Position(10, 10, 90))

    plot_position(initial_pos=Position(0, 0, 90), final_pos=Position(10, 10, 0))

    plot_position(initial_pos=Position(0, 0, 45), final_pos=Position(10, 10, 90))

    plot_position(initial_pos=Position(0, 0, 0), final_pos=Position(10, 10, 90))

    plt.show()

    pass


if __name__ == '__main__':
    main()
