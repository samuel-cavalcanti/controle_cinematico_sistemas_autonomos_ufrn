# Make sure to have the server side running in CoppeliaSim:
# in a child script of a CoppeliaSim scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!


from ctypes import pointer
from typing import Optional
import sim
import math


def connect_to_coppelia_sim(port: int) -> int:

    sim.simxFinish(-1)  # just in case, close all opened connections

    wait_until_connect = True
    do_not_reconnect_once_disconnect = True
    time_out_in_ms = 5000
    conn_thread_cycle = 5

    client_id = sim.simxStart('127.0.0.1', port, wait_until_connect, do_not_reconnect_once_disconnect,
                              time_out_in_ms, conn_thread_cycle)  # Connect to CoppeliaSim

    if client_id == -1:
        print('Não foi possível conectar com o simulador')
        exit(-1)

    return client_id


def get_motors(client_id: int) -> tuple[int, int]:
    '''
        sim.getObjectHandle("Pioneer_p3dx_leftMotor")
    '''

    left_motor_name = 'Pioneer_p3dx_leftMotor'
    right_motor_name = 'Pioneer_p3dx_rightMotor'

    blocking_mode = sim.simx_opmode_blocking
    _, left_motor = sim.simxGetObjectHandle(
        client_id, left_motor_name, blocking_mode)

    _, right_motor = sim.simxGetObjectHandle(
        client_id, right_motor_name, blocking_mode)

    assert right_motor != -1,\
        f'não foi possível recuperar o motor direito do simulador: {right_motor_name}'
    assert left_motor_name != -1,\
        f'não foi possível recuperar o motor esquerdo do simulador: {left_motor_name} '

    return left_motor, right_motor


def get_sensors(client_id: int) -> list[int]:
    '''
        for i=1,16,1 do
            usensors[i]=sim.getObjectHandle("Pioneer_p3dx_ultrasonicSensor"..i)
        end
    '''
    sensors = list()
    blocking_mode = sim.simx_opmode_blocking
    for i in range(1, 17):
        sensor_name = f'Pioneer_p3dx_ultrasonicSensor{i}'

        _, proximity_sensor = sim.simxGetObjectHandle(
            client_id, sensor_name, blocking_mode)

        assert proximity_sensor != -1, \
            f'não foi possível recuperar o sensor: {sensor_name}'

        sensors.append(proximity_sensor)

    assert len(sensors) == 16, "O número total dos sensores deve ser 16 "

    return sensors


def read_sensors(client_id: int, sensors: list[int]) -> list[float]:

    distances = list()

    for sensor in sensors:

        return_code, detection_state, values, _, _ = sim.simxReadProximitySensor(
            client_id, sensor, sim.simx_opmode_streaming)

        if return_code == sim.simx_return_ok:
            distance = 1.0 if detection_state == False else values[2]

            distances.append(distance)

    return distances


def set_motor_velocity(client_id: int, motor_id: int, velocity: float):
    sim.simxSetJointTargetVelocity(
        client_id, motor_id, velocity, sim.simx_opmode_streaming)


def pioneer_controller(distances: list[float]) -> tuple[float, float]:

    no_detection_dist = 0.5
    max_detection_dist = 0.2

    delta_detection_dist = no_detection_dist - max_detection_dist

    v_0 = 2

    braitenberg_left = [-0.2, -0.4, -0.6, -0.8, -1, -1.2, -
                        1.4, -1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    braitenberg_right = [-1.6, -1.4, -1.2, -1, -0.8, -
                         0.6, -0.4, -0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    detect = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for index, distance in enumerate(distances):

        if distance < no_detection_dist:

            if distance < max_detection_dist:
                distance = max_detection_dist

            detect[index] = 1 - \
                ((distance-max_detection_dist)/delta_detection_dist)

        else:
            detect[index] = 0

    v_left = v_0
    v_right = v_0

    for b_left, b_right, detect_value in zip(braitenberg_left, braitenberg_right, detect):
        v_left = b_left*detect_value + v_left
        v_right = b_right*detect_value + v_right

    return v_left, v_right


def get_robot_position(client_id: int, robot: int) -> Optional[list[float]]:
    '''Retorna a posição do robo referente ao referencial global'''
    return_code, position = sim.simxGetObjectPosition(
        client_id, robot, -1, sim.simx_opmode_streaming)

    if return_code == sim.simx_return_ok:
        return position

    return None


def get_robot_orientation(client_id: int, robot: int) -> Optional[list[float]]:
    '''Retorna os angulos de euler: yaw , pitch, roll referente ao referencial global'''

    return_code, orientation = sim.simxGetObjectOrientation(
        client_id, robot, -1, sim.simx_opmode_streaming)

    if return_code == sim.simx_return_ok:
        return orientation

    return None


def euler_angles_to_rotation_matrix(angles: list[float]) -> list[list[float]]:
    '''
    |(cos(b)*cos(g))                                    (cos(b)*(-sin(g)))                                  sin(b)                                             |
    |sin(a))*sin(b)*cos(g) + cos(a)*sin(g)              cos(a)cos(g) - sin(a)sin(b)sin(g)                 -sin(a)*cos(b)                                |
    | (-cos(a)*sin(b) )*cos(g) + sin(a)*sin(g)    cos(a)*sin(b)*sin(g)+ sin(a)*cos(g)    cos(a)*cos(b)                                    | 
    '''
    alpha_in_rads = angles[0]
    beta_in_rads = angles[1]
    gamma_in_rads = angles[2]

    # return [
    #     [
    #         math.cos(beta_in_rads)*math.cos(gamma_in_rads),
    #         -math.cos(beta_in_rads)*math.sin(gamma_in_rads),
    #         math.sin(beta_in_rads)
    #     ],
    #     [
    #         math.sin(alpha_in_rads)*math.sin(beta_in_rads)*math.cos(gamma_in_rads) + math.cos(alpha_in_rads)*math.sin(gamma_in_rads),
    #         math.cos(alpha_in_rads)*math.cos(gamma_in_rads) -math.sin(alpha_in_rads)*math.sin(beta_in_rads)*math.sin(gamma_in_rads),
    #         - math.sin(alpha_in_rads)* math.cos(beta_in_rads)  

    #     ],
    #     [
    #         (-math.cos(alpha_in_rads)*math.sin(beta_in_rads) )*math.cos(gamma_in_rads) + math.sin(alpha_in_rads)*math.sin(gamma_in_rads),
    #         math.cos(alpha_in_rads)*math.sin(beta_in_rads)*math.sin(gamma_in_rads) + math.sin(alpha_in_rads)*math.cos(gamma_in_rads),
    #         math.cos(alpha_in_rads)*math.cos(beta_in_rads)

    #     ]
    # ]

def orientetation_theta(angles: list[float]) -> float:
    alpha_in_rads = angles[0]
    beta_in_rads = angles[1] 
    gamma_in_rads = angles[2]
    return (2 * math.acos(math.cos((alpha_in_rads + gamma_in_rads)/2) * math.cos(beta_in_rads/2)))

def main():
    client_id = connect_to_coppelia_sim(port=19999)

    left_motor, right_motor = get_motors(client_id)

    proximity_sensors = get_sensors(client_id)

    _, pionner = sim.simxGetObjectHandle(
        client_id, 'Graph', sim.simx_opmode_blocking)

    assert pionner != -1, 'Não conseguiu achar o pionner'

    '''
        Posição inicial do robô:
             x: -1.2945 metros
             y:  0.050001 metros
             z:  0.13879 metros

         

    '''

    # alpha = 0
    # beta = 0
    # gamma = 0

    while sim.simxGetConnectionId(client_id) != -1:
        distances = read_sensors(client_id, proximity_sensors)

        velocity_left, velocity_right = pioneer_controller(distances)

        euler_angles = get_robot_orientation(client_id, pionner)

        if euler_angles:
            # rotation_matrix = euler_angles_to_rotation_matrix(euler_angles)
            orientation_robo = orientetation_theta(euler_angles)
            print('Orientação do Robo(Theta): ', ((orientation_robo*180)/math.pi))
            # for line in rotation_matrix:
            #     print(line)

        position = get_robot_position(client_id, pionner)

        print('position: ', position)
        print('euler angles: ', euler_angles)



        set_motor_velocity(client_id, left_motor, velocity_left)
        set_motor_velocity(client_id, right_motor, velocity_right)


if __name__ == '__main__':

    main()
