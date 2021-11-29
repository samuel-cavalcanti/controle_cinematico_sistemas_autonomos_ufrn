import time

import controllers
import coppeliasim
import utils
from path_planning import path_by_polynomials
from utils import Position


def draw_path(client_id: int, initial_pos: Position, final_pos: Position):
    x_coefficients, y_coefficients = path_by_polynomials.find_coefficients(initial_pos, final_pos)
    p_x, p_y, theta_t = path_by_polynomials.create_path_functions(x_coefficients, y_coefficients)

    path_points = path_by_polynomials.path_points_generator(p_x, p_y)

    coppeliasim.send_path_4_drawing(path_points, client_id)


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
    final = utils.Position(2.1, 2.1, utils.deg2rad(90))
    initial_time = time.time()
    current_time = time.time() - initial_time
    max_time_in_seconds = 5.0
    controller = controllers.PathFollowController(initial_pos=initial,
                                                  desired_pos=final,
                                                  initial_time_in_seconds=current_time,
                                                  max_time=max_time_in_seconds)

    draw_path(client_id, initial_pos=initial, final_pos=final)

    while coppeliasim.simulation_is_alive(client_id):

        euler_angles_in_rads = coppeliasim.get_robot_orientation(client_id, pioneer)
        position = coppeliasim.get_robot_position(client_id, pioneer)

        if euler_angles_in_rads and position:
            theta_in_rads = euler_angles_in_rads[2]
            x = position[0]
            y = position[1]
            current_pos = utils.Position(x, y, theta_in_rads)
            current_time = time.time() - initial_time
            pioneer_velocity = controller.step(current_pos, current_time)

            if current_time > max_time_in_seconds:
                break
            coppeliasim.set_motor_velocity(client_id, left_motor, pioneer_velocity.left)
            coppeliasim.set_motor_velocity(client_id, right_motor, pioneer_velocity.right)


if __name__ == '__main__':
    main()
