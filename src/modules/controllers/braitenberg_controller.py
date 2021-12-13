from modules.robots_kinematics.pioneer import PioneerWheelVelocity

"""
       Controlador que desvia de obstáculos do Pioneer. Quando se insere um Pioneer em uma simulação
       ele já vem com esse controlador,mas escrito em LUA. Foi passado esse Algoritmo para Python
       para fins de testar o Legacy Remote-API
"""

NO_DETECTION_DIST = 0.5
MAX_DETECTION_DIST = 0.2

BRAITENBERG_LEFT = [-0.2, -0.4, -0.6, -0.8, -1, -1.2, -1.4, -1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

BRAITENBERG_RIGHT = [-1.6, -1.4, -1.2, -1, -0.8, -0.6, -0.4, -0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


def braitenberg_controller(sonar_distances: list[float]) -> PioneerWheelVelocity:
    delta_detection_dist = NO_DETECTION_DIST - MAX_DETECTION_DIST

    v_0 = 2

    detect = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for index, distance in enumerate(sonar_distances):

        if distance < NO_DETECTION_DIST:

            if distance < MAX_DETECTION_DIST:
                distance = MAX_DETECTION_DIST

            detect[index] = 1 - ((distance - MAX_DETECTION_DIST) / delta_detection_dist)

        else:
            detect[index] = 0

    v_left = v_0
    v_right = v_0

    for b_left, b_right, detect_value in zip(BRAITENBERG_LEFT, BRAITENBERG_RIGHT, detect):
        v_left = b_left * detect_value + v_left
        v_right = b_right * detect_value + v_right

    return PioneerWheelVelocity(right=v_right, left=v_left)
