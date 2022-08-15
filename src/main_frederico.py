import time
from pathlib import Path

import numpy as np

from modules import coppeliasim, controllers
from modules.utils import Position, PID
from modules.simulation_recorder import SimulationRecorder, SimulationCSVRecorder


def is_arrival(current: Position, desired: Position) -> bool:
    precision_in_meters = 0.05
    arrival_x = np.abs(current.x - desired.x) <= precision_in_meters
    arrival_y = np.abs(current.y - desired.y) <= precision_in_meters
    return arrival_x and arrival_y


def create_federico_controller() -> controllers.FredericoController:
    k_p = 0.9145
    k_i = k_p / 1.9079
    k_d = k_p * 0.085
    """Constantes Kp Ki Kd adquiridas experimentalmente """
    pid_position = PID(k_p, k_i, k_d, set_point=0)
    k_p = 0.4
    k_i = 0.15
    k_d = k_p * 0.0474
    pid_orientation = PID(k_p, k_d, k_i, set_point=0)
    controller = controllers.FredericoController(position_controller=pid_position,
                                                 orientation_controller=pid_orientation)

    return controller


def main():
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

    final = Position(2.1, 2.1, np.deg2rad(45))

    federico_controller = create_federico_controller()

    initial_time = time.time()

    coppeliasim.set_object_position(
        client_id, target, [final.x, final.y, +2.3879e-01])

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

    simulation_recorder: SimulationRecorder = SimulationCSVRecorder(
        headers=simulation_sample_header)

    while coppeliasim.simulation_is_alive(client_id):
        current_time = time.time() - initial_time

        euler_angles_in_rads = coppeliasim.get_object_orientation(client_id, pioneer)
        position = coppeliasim.get_object_position(client_id, pioneer)

        velocity = coppeliasim.get_object_velocity(client_id, pioneer)

        if not position or not euler_angles_in_rads or not velocity:
            continue

        current_pos = Position(
            x=position[0],
            y=position[1],
            theta_in_rads=euler_angles_in_rads[2])

        linear_velocity, angular_velocity = velocity

        current_sample = [linear_velocity[0],
                          linear_velocity[1],
                          angular_velocity[2],
                          current_pos.x,
                          current_pos.y,
                          current_pos.theta_in_rads,
                          final.x,
                          final.y,
                          final.theta_in_rads,
                          current_time]

        simulation_recorder.add_sample(current_sample)

        if is_arrival(current=current_pos, desired=final):
            coppeliasim.set_motor_velocity(client_id, left_motor, 0.0)
            coppeliasim.set_motor_velocity(client_id, right_motor, 0.0)
            break
        else:
            pioneer_velocity = federico_controller.step(
                current_pos, desired_pos=final)
            coppeliasim.set_motor_velocity(
                client_id, left_motor, pioneer_velocity.left)
            coppeliasim.set_motor_velocity(
                client_id, right_motor, pioneer_velocity.right)

    simulation_recorder.save(Path('output').joinpath('main_frederico.csv'))


if __name__ == '__main__':
    main()
