from dataclasses import dataclass

import numpy as np

B = 2.521817003775056


@dataclass
class PioneerWheelVelocity:
    """ Velocidade do Pioneer em Rad/s"""
    right: float
    left: float


@dataclass
class PioneerVelocity:
    x: float
    y: float
    omega: float


def inverse_kinematic(theta_in_rads: float, velocity: np.ndarray) -> PioneerWheelVelocity:
    """
    theta é o ângulo de orientação do robô em relação ao referencial global em radianos

    velocity é o vetor de velocidade do robô sendo:
        velocity[0] é o a velocidade linear em relação ao eixo x em radianos
        velocity[1] é o a velocidade linear em relação ao eixo y em radianos
        velocity[2] é a velocidade angular do robô em radianos, geralmente representado pela letra grega omega

    a saída é velocidade das rodas do Pioneer
    """

    linear_velocity = velocity[0] * np.cos(theta_in_rads) + velocity[1] * np.sin(theta_in_rads)
    angular_velocity = 1 / 2 * B * velocity[2]

    right_wheel = angular_velocity + linear_velocity
    left_wheel = -angular_velocity + linear_velocity

    return PioneerWheelVelocity(right=right_wheel, left=left_wheel)


def direct_kinematic(left_wheel_in_rads: float, right_wheel_in_rads: float, theta_in_rads: float) -> PioneerVelocity:
    mean = (left_wheel_in_rads + right_wheel_in_rads) / 2

    delta_x = np.cos(theta_in_rads) * mean
    delta_y = np.sin(theta_in_rads) * mean
    delta_theta = (right_wheel_in_rads - left_wheel_in_rads) / B

    return PioneerVelocity(x=delta_x, y=delta_y, omega=delta_theta)
