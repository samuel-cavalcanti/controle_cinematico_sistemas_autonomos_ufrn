from pathlib import Path
from modules import controllers
from modules.coppeliasim import remote_api as coppeliasim

from modules.simulation_recorder.simulation_csv_recorder import SimulationCSVRecorder
from modules.simulation_recorder.simulation_recorder import SimulationRecorder
import os


def main():
    client_id = coppeliasim.try_to_connect_to_coppeliasim(port=19999)

    left_motor, right_motor = coppeliasim.get_motors(client_id)

    proximity_sensors = coppeliasim.get_sensors(client_id)

    pioneer = coppeliasim.get_pioneer_p3dx(client_id)

    header_sensors = [f'distância do sensor {i} em metros' for i in range(len(proximity_sensors))]

    header_robot = [
        'posição x do robô em metros',
        'posição y do robô em metros',
        'orientação do robô em rads',
    ]

    recorder: SimulationRecorder = SimulationCSVRecorder(headers=header_robot + header_sensors)

    while coppeliasim.simulation_is_alive(client_id):

        distances = coppeliasim.read_sensors(client_id, proximity_sensors)
        position = coppeliasim.get_object_position(client_id, pioneer)
        euler_angles_in_rads = coppeliasim.get_object_orientation(client_id, pioneer)
        if distances is None or position is None or euler_angles_in_rads is None:
            continue

        robot_sample = [
            position[0],
            position[1],
            euler_angles_in_rads[2],
        ]
        recorder.add_sample(sample=robot_sample + distances)

        pioneer_velocity = controllers.braitenberg_controller(distances)
        coppeliasim.set_motor_velocity(client_id, left_motor, pioneer_velocity.left)
        coppeliasim.set_motor_velocity(client_id, right_motor, pioneer_velocity.right)

    create_output_dir()
    recorder.save(Path('output').joinpath('brainterberg_simulation.csv'))

def create_output_dir():
    output_dir = 'output'
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)


if __name__ == '__main__':
    main()
