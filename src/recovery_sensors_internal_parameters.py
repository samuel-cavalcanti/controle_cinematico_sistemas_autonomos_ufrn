"""
    Esse script visa buscar e salvar os parâmetros do sensores para o cálculo
    do modelo inverso do sensor. Para isso foi carrego qualquer uma dos cenários
    de simulação do CoppeliaSim e posicionado o Pioneer P3dx  no centro do cenário
    e executado esse script
"""

from pathlib import Path
from modules.coppeliasim import remote_api as coppeliasim

from modules.utils import Position
from modules.mapping.inverse_sensor_model import UltrasonicInternalParameters
import numpy as np
import dataclasses
import json


def main():

    print('tentando se conectar ao simulador')
    client_id = coppeliasim.try_to_connect_to_coppeliasim(port=19997)

    proximity_sensors = coppeliasim.get_sensors(client_id)

    if not coppeliasim.simulation_is_alive(client_id):
        print('a Simulação precisa está ativa')

    print('conectado ao simulador')
    print('Extraindo valores de posição e orientação dos sensores do simulador')

    def get_position_and_orientation() -> tuple[list[list[float]], list[list[float]]]:
        simulation_positions = [coppeliasim.get_object_position(client_id, sensor) for sensor in proximity_sensors]
        simulation_orientations = [coppeliasim.get_object_orientation(client_id, sensor) for sensor in proximity_sensors]
        while None in simulation_positions or None in simulation_orientations:
            simulation_positions = [coppeliasim.get_object_position(client_id, sensor) for sensor in proximity_sensors]
            simulation_orientations = [coppeliasim.get_object_orientation(client_id, sensor) for sensor in proximity_sensors]
   
        return simulation_positions, simulation_orientations  # type: ignore

    simulation_positions, simulation_orientations = get_position_and_orientation()    

    def map_to_position(simulation_position: list[float], euler_angles_in_rads: list[float]) -> Position:
        """No caso do sensores o angulo theta é o angulo beta do simulador"""
        return Position(x=simulation_position[0], y=simulation_position[1], theta_in_rads=euler_angles_in_rads[1])

    print('Salvando as informações dos sensores em um arquivo JSON na pasta Output')

    positions = [map_to_position(sim_p, sim_o) for sim_p, sim_o in zip(simulation_positions, simulation_orientations)]

    """
        Todos so sensores são iguais e possuem os mesmos parâmetros internos
        Os parâmetros foram retirados olhando as configurações internas dos sensores
        no simulador
    """
    params = UltrasonicInternalParameters(
        alpha_in_rads=np.deg2rad(30),
        max_distance_in_meters=1,
        min_distance_in_meters=0.05,
        e_in_meters=0  # não foi encontrado o parâmetro: "e" do slide Mapeamento.pdf página 27
    )

    sensors_dict = dict()

    for index in range(len(proximity_sensors)):
        key = f'Pioneer_p3dx_ultrasonicSensor{index+1}'
        sensors_dict[key] = dataclasses.asdict(positions[index])

    sensors_dict['ultrasonic_internal_parameters'] = dataclasses.asdict(params)

    json_string = json.dumps(sensors_dict)

    output_file = Path('output').joinpath('sensors_internal_parameters.json')

    with open(output_file, 'w') as json_file:
        json_file.write(json_string)

    print('Arquivo JSON salvo com sucesso')


if __name__ == '__main__':
    main()
