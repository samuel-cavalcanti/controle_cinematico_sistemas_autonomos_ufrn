from email import header
from pathlib import Path
import numpy as np
import json
import sys
import os

try:
    from src.modules.utils import Position
except ModuleNotFoundError:
    sys.path.append(os.getcwd())
    from src.modules.utils import Position
from src.modules.mapping.inverse_sensor_model import UltrasonicInverseModel, UltrasonicInternalParameters
from src.modules.mapping.occupancy_grid_mapping import OccupancyGridMapping
from src.modules.mapping.robot_state import RobotState
from src.modules.grid import OccupancyGrid, GridLimits
from src.modules.mapping import robot_state
from src.modules.utils.plotter_2d import Plotter2D


def remove_replicates():
    print('loading data')
    simulation_data_file = Path('output').joinpath('brainterberg_simulation.csv')
    simulation_data = np.loadtxt(simulation_data_file, delimiter=',', skiprows=1)
    print('starting to filter')
    filtered_data = dict()

    def calcule_hash(sample: np.ndarray) -> int:
        string = '-'.join([str(col) for col in sample])
        return hash(string)

    for sample in simulation_data:
        key = calcule_hash(sample)
        filtered_data[key] = sample

    values = list(filtered_data.values())
    simulation_data_file = Path('output').joinpath('brainterberg_simulation_filtered.csv')
    header_row = 'posição x do robô em metros,posição y do robô em metros,orientação do robô em rads,distância do sensor 0 em metros,distância do sensor 1 em metros,distância do sensor 2 em metros,distância do sensor 3 em metros,distância do sensor 4 em metros,distância do sensor 5 em metros,distância do sensor 6 em metros,distância do sensor 7 em metros,distância do sensor 8 em metros,distância do sensor 9 em metros,distância do sensor 10 em metros,distância do sensor 11 em metros,distância do sensor 12 em metros,distância do sensor 13 em metros,distância do sensor 14 em metros,distância do sensor 15 em metros'

    print('saving .csv')
    np.savetxt(simulation_data_file, np.array(values), delimiter=',', header=header_row)


def main():

    sensors_data = load_json(Path('output').joinpath('sensors_internal_parameters.json'))

    params = UltrasonicInternalParameters(**sensors_data['ultrasonic_internal_parameters'])
    del sensors_data['ultrasonic_internal_parameters']

    def json_data_to_ultrasonic_inverse_model(sensor_name: str):
        sensor_pos = Position(**sensors_data[sensor_name])
        return UltrasonicInverseModel(sensor_pos, params)

    models = [json_data_to_ultrasonic_inverse_model(sensor_name) for sensor_name in sensors_data]

    grid_limits = GridLimits(x_min=-2.1850e+00, x_max=2.1850e+00, y_min=-2.2506e+00, y_max=2.2506e+00, resolution=0.1)

    grid = OccupancyGrid(grid_limits)
    

    mapping = OccupancyGridMapping(occupancy_grid=grid, ultrasonics=models)

    simulation_data_file = Path('output').joinpath('brainterberg_simulation_filtered.csv')
    simulation_data = np.loadtxt(simulation_data_file, delimiter=',', skiprows=1)

    for index, sample in enumerate(simulation_data):
        position = Position(x=sample[0],
                            y=sample[1],
                            theta_in_rads=sample[2])

        distances = sample[3:].tolist()

        robot_state = RobotState(robot_pos=position,
                                 normalized_distances=distances)

        mapping.one_it(robot_state)

        print(f'\r executed: {index +1} of {len(simulation_data)}',end='')
        if index == 5:
            break
    


       
       
    plotter = Plotter2D()

    image = grid.get_probability_matrix()

    print([line for line in image])
    print(image.shape)

    plotter.draw_image(image)

    plotter.show()


def load_json(file_path: Path) -> list[dict]:

    with open(file_path) as json_file:
        return json.loads(json_file.read())


if __name__ == '__main__':
    main()
    # remove_replicates()
