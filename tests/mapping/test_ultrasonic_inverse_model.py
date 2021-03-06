import unittest

from src.modules.mapping.inverse_sensor_model import UltrasonicInverseModel, UltrasonicInternalParameters, Space
from src.modules.mapping.inverse_sensor_model.sensor_state import SensorState
from src.modules.utils.position import Position
import numpy as np


class UltrasonicInverseModelTestCase(unittest.TestCase):

    def test_inverse_model(self):

        sensor_pos = Position(x=0, y=0, theta_in_rads=0)
        sensor_parameters = UltrasonicInternalParameters(
            alpha_in_rads=np.deg2rad(30),
            e_in_meters=0.01,
            max_distance_in_meters=1,
            min_distance_in_meters=0.05)

        """
             ---------    | 1 metrô de raio
             \       /    | e 30 graus de abertura
              \     /     | valores menores que 0.05 metros não são detectáveis
               \   /      |      
                \ /       |
                 . (robô) |        

        """

        sensor_model = UltrasonicInverseModel(sensor_pos, sensor_parameters)

        states = [
            SensorState(robot_position=Position(0, 0, 0), normalized_distance=1.0),  # 0
            SensorState(robot_position=Position(0.5, 0.5, 0), normalized_distance=1.0),  # 1
            SensorState(robot_position=Position(1.0, 1.0, 0), normalized_distance=1.0),  # 2
            SensorState(robot_position=Position(1.0, 1.0, np.deg2rad(20)), normalized_distance=1.0),  # 3
            SensorState(robot_position=Position(1.0, 1.0, np.deg2rad(40)), normalized_distance=1.0),  # 4
            SensorState(robot_position=Position(1.0, 1.0, np.deg2rad(40)), normalized_distance=0.5),  # 5
            SensorState(robot_position=Position(1.3, 1.3, np.deg2rad(40)), normalized_distance=0.5),  # 6
        ]

        expected_spaces = [
            Space.out_of_range,  # 0
            Space.out_of_range,  # 1
            Space.out_of_range,  # 2
            Space.out_of_range,  # 3
            Space.free,  # 4
            Space.out_of_range,  # 5
            Space.free  # 6
        ]

                                                
        for state, space in zip(states, expected_spaces):
            result_space = sensor_model.inverse_model(sensor_state=state, grid_center=(1.5, 1.5))
            self.assertEqual(result_space, space,
                              msg=f'expected: {space} result {result_space}')
