import numpy as np

import controllers
import coppeliasim
import utils
from path_planning import path_by_polynomials
from utils import Position, PID


def draw_path(client_id: int, initial_pos: Position, final_pos: Position):
    x_coefficients, y_coefficients = path_by_polynomials.find_coefficients(initial_pos, final_pos)
    p_x, p_y, theta_t = path_by_polynomials.create_path_functions(x_coefficients, y_coefficients)

    path_points = path_by_polynomials.path_points_generator(p_x, p_y)

    coppeliasim.send_path_4_drawing(path_points, client_id)


def is_arrival(current: Position, desired: Position) -> bool:
    precision = 0.1
    arrival_x = np.abs(current.x - desired.x) <= precision
    arrival_y = np.abs(current.y - desired.y) <= precision
    return arrival_x and arrival_y


def create_federico_controller() -> controllers.FredericoController:
    k_p = 0.9145
    k_i = k_p / 1.9079
    k_d = k_p * 0.085
    """Constantes Kp Ki Kd retiradas da tese de Federico"""
    pid_position = PID(k_p, k_i, k_d, set_point=0)
    k_p = 0.4
    k_d = k_p * 0.0474
    k_i = 0.15
    pid_orientation = PID(k_p, k_d, k_i, set_point=0)
    controller = controllers.FredericoController(position_controller=pid_position,
                                                 orientation_controller=pid_orientation)

    return controller


def main():
    client_id = coppeliasim.connect_to_coppelia_sim(port=19999)

    left_motor, right_motor = coppeliasim.get_motors(client_id)

    pioneer = coppeliasim.get_pioneer_p3dx(client_id)
    '''
           Posição inicial do robô:
                x: -1.2945 metros
                y:  0.050001 metros
                z:  0.13879 metros

           orientação inicial do robô angulos de euler:
               alpha = 0 radiano
               beta = 0 radiano
               gamma = 0 radiano
       '''

    initial = utils.Position(x=-1.2945, y=0.050001, theta_in_rads=0)
    final = utils.Position(2.1, 2.1, utils.deg2rad(45))

    federico_controller = create_federico_controller()

    draw_path(client_id, initial_pos=initial, final_pos=final)

    while coppeliasim.simulation_is_alive(client_id):

        euler_angles_in_rads = coppeliasim.get_robot_orientation(client_id, pioneer)
        position = coppeliasim.get_robot_position(client_id, pioneer)

        if euler_angles_in_rads and position:
            theta_in_rads = euler_angles_in_rads[2]
            x = position[0]
            y = position[1]
            current_pos = utils.Position(x, y, theta_in_rads)

            if is_arrival(current=current_pos, desired=final):
                coppeliasim.set_motor_velocity(client_id, left_motor, 0.0)
                coppeliasim.set_motor_velocity(client_id, right_motor, 0.0)
            else:
                pioneer_velocity = federico_controller.step(current_pos, desired_pos=final)
                coppeliasim.set_motor_velocity(client_id, left_motor, pioneer_velocity.left)
                coppeliasim.set_motor_velocity(client_id, right_motor, pioneer_velocity.right)


if __name__ == '__main__':
    main()
