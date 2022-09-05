import time
from pathlib import Path
import numpy as np
from modules import controllers
from modules.coppeliasim import remote_api as coppeliasim

from modules.path_and_trajectory_planning.path_follow import PathFollow
from modules.utils import Position, PID
from modules.simulation_recorder import SimulationRecorder, SimulationCSVRecorder

import sys


def draw_path(client_id: int, path: np.ndarray):

    path_points = list()
    for point in path:
        path_points.append(point[0])
        path_points.append(point[1])
        path_points.append(0.05)

    coppeliasim.send_path_4_drawing(path_points, client_id)


def create_federico_controller() -> controllers.FredericoController:
    k_p = 0.5145
    k_i = k_p / 2.9079
    k_d = k_p * 0.085
    """Constantes Kp Ki Kd retiradas da tese de Federico"""
    pid_position = PID(k_p, k_i, k_d, set_point=0)
    k_p = 0.7
    k_d = k_p * 0.0174
    k_i = 0.15
    pid_orientation = PID(k_p, k_d, k_i, set_point=0)
    controller = controllers.FredericoController(position_controller=pid_position,
                                                 orientation_controller=pid_orientation)

    return controller


def load_path_from_csv_file(csv_file: Path) -> np.ndarray:
    return np.loadtxt(csv_file, delimiter=',')


def main():
    command_line_chooses = {'p_space': 'a_star_potential_field_path', 'c_space': 'a_star__c_space'}
    file_name = command_line_chooses.get(sys.argv[1], command_line_chooses['p_space'])
    path_csv_file = Path('assets').joinpath('paths').joinpath(f'{file_name}.csv')
    path = load_path_from_csv_file(path_csv_file)

    path_follow = PathFollow(path)

    client_id = coppeliasim.try_to_connect_to_coppeliasim(port=19999)

    left_motor, right_motor = coppeliasim.get_motors(client_id)

    pioneer = coppeliasim.get_pioneer_p3dx(client_id)

    target = coppeliasim.get_target(client_id)

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

    initial_time = time.time()
    current_time = time.time() - initial_time

    simulation_sample_header = ['linear_velocity_x',
                                'linear_velocity_y',
                                'angular_velocity_theta',
                                'current_pos_x',
                                'current_pos_y',
                                'current_pos_theta',
                                'desired_pos_x',
                                'desired_pos_y',
                                'desired_pos_theta',
                                'time_in_seconds'
                                ]

    simulation_recorder: SimulationRecorder = SimulationCSVRecorder(headers=simulation_sample_header)

    controller = create_federico_controller()

    draw_path(client_id, path=path)

    while coppeliasim.simulation_is_alive(client_id):
        current_time = time.time() - initial_time

        euler_angles_in_rads = coppeliasim.get_object_orientation(
            client_id, pioneer)
        position = coppeliasim.get_object_position(client_id, pioneer)

        velocity = coppeliasim.get_object_velocity(client_id, pioneer)

        if not velocity or not position or not euler_angles_in_rads:
            continue

        current_pos = Position(
            x=position[0],
            y=position[1],
            theta_in_rads=euler_angles_in_rads[2])

        linear_velocity, angular_velocity = velocity

        desired_pos = path_follow.step(current_pos)

        pioneer_velocity = controller.step(current_pos, desired_pos)

        current_sample = [linear_velocity[0],
                          linear_velocity[1],
                          angular_velocity[2],
                          current_pos.x,
                          current_pos.y,
                          current_pos.theta_in_rads,
                          desired_pos.x,
                          desired_pos.y,
                          desired_pos.theta_in_rads,
                          current_time]

        simulation_recorder.add_sample(current_sample)

        if path_follow.is_ended():
            coppeliasim.set_motor_velocity(client_id, left_motor, 0)
            coppeliasim.set_motor_velocity(client_id, right_motor, 0)
            break

        coppeliasim.set_motor_velocity(
            client_id, left_motor, pioneer_velocity.left)
        coppeliasim.set_motor_velocity(
            client_id, right_motor, pioneer_velocity.right)
        coppeliasim.set_object_position(
            client_id, target, [desired_pos.x, desired_pos.y, +2.3879e-01])

    simulation_recorder.save(Path('output').joinpath(f'main_path_follow_{file_name}.csv'))


if __name__ == '__main__':
    main()
