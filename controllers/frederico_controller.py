import numpy as np

from robots_kinematics import pioneer
from robots_kinematics.pioneer import PioneerWheelVelocity
from utils import Position, euclidean_distance
from utils.pid import PID


class FredericoController:
    __position_controller: PID
    __orientation_controller: PID

    def __init__(self, position_controller: PID, orientation_controller: PID):
        """
            Esse Controlador buscar chegar no ponto de referência independente da sua orientação, para isso ele utiliza
            um PID que envia sinal de velocidade linear e um PID que envia sinal de velocidade angular, o PID que envia
            sinal de velocidade linear busca minimizar a distância da posição do robô para a distância próxima desejada.
            O PID que envia sinais de velocidade angular busca modificar a orientação do robô para que essa distância
            próxima seja a distância real entre o robô o seu alvo.
         """
        self.__position_controller = position_controller
        self.__orientation_controller = orientation_controller

    def step(self, current: Position, desired_pos: Position) -> PioneerWheelVelocity:
        """Calculo da referencia"""
        delta_x = desired_pos.x - current.x
        delta_y = desired_pos.y - current.y
        delta_l = euclidean_distance(delta_x, delta_y)
        phi = np.arctan2(delta_y, delta_x)
        delta_phi =  phi - current.theta_in_rads

        """Controladores desacoplados"""
        linear_velocity_in_polar_system = self.__position_controller.step(delta_l * np.cos(delta_phi))
        angular_velocity = self.__orientation_controller.step(delta_phi)

        """Transformando o sistema polar para cartesiano"""
        x = linear_velocity_in_polar_system * np.cos(current.theta_in_rads)
        y = linear_velocity_in_polar_system * np.sin(current.theta_in_rads)

        q = np.array([x, y, angular_velocity])

        return pioneer.inverse_kinematic(theta_in_rads=current.theta_in_rads, velocity=q)
