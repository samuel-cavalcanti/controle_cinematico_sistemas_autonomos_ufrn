import controllers
import coppeliasim

import utils


def main():
    client_id = coppeliasim.connect_to_coppelia_sim(port=19999)

    left_motor, right_motor = coppeliasim.get_motors(client_id)

    proximity_sensors = coppeliasim.get_sensors(client_id)

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

    initial_pos = utils.Position(x=-1.2945, y=0.050001, theta_in_degree=0)
    final_pos = utils.Position(2.1, 2.1, 45)

    x_coefficients, y_coefficients = utils.find_coefficients(initial_pos, final_pos)
    p_x, p_y, theta_t = utils.create_path_functions(x_coefficients, y_coefficients)

    path_points = utils.path_points_generator(p_x, p_y, theta_t)

    coppeliasim.send_path_4_drawing(path_points, client_id)

    while coppeliasim.simulation_is_alive(client_id):

        distances = coppeliasim.read_sensors(client_id, proximity_sensors)

        if distances:
            velocity_left, velocity_right = controllers.braitenberg_controller(distances)

            # coppeliasim.set_motor_velocity(client_id, left_motor, velocity_left)
            # coppeliasim.set_motor_velocity(client_id, right_motor, velocity_right)

        euler_angles_in_rads = coppeliasim.get_robot_orientation(client_id, pioneer)

        if euler_angles_in_rads:
            robot_orientation = utils.orientation_theta(euler_angles_in_rads)
            # print('euler angles: ', euler_angles_in_rads)
            # print('Orientação do Robo(Theta): ', utils.rad2deg(robot_orientation))

        position = coppeliasim.get_robot_position(client_id, pioneer)


if __name__ == '__main__':
    main()
