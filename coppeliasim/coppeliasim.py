from typing import Optional

from . import sim

"""
 Make sure to have the server side running in CoppeliaSim:
 in a child script of a CoppeliaSim scene, add following command
 to be executed just once, at simulation start:

 simRemoteApi.start(19999)

 then start simulation, and run this program.

 IMPORTANT: for each successful call to simxStart, there
 should be a corresponding call to simxFinish at the end!
"""


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

    assert right_motor != -1, \
        f'não foi possível recuperar o motor direito do simulador: {right_motor_name}'
    assert left_motor_name != -1, \
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


def read_sensors(client_id: int, sensors: list[int]) -> Optional[list[float]]:
    distances = list()

    for sensor in sensors:

        return_code, detection_state, values, _, _ = sim.simxReadProximitySensor(
            client_id, sensor, sim.simx_opmode_streaming)

        if return_code == sim.simx_return_ok:
            distance = 1.0 if not detection_state else values[2]
            distances.append(distance)
        else:
            return None

    return distances


def set_motor_velocity(client_id: int, motor_id: int, velocity: float):
    sim.simxSetJointTargetVelocity(
        client_id, motor_id, velocity, sim.simx_opmode_streaming)


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


def simulation_is_alive(client_id: int) -> bool:
    '''
        Verifica se a simulação ainda está rodando, no caso quando alguém apertar o botão de Stop
        essa função retorna FALSE.Se a simulação estiver pausada,a função também retorna True
    '''
    return sim.simxGetConnectionId(client_id) != -1


def stop_simulation(client_id: int):
    sim.simxStopSimulation(client_id, sim.simx_opmode_blocking)


def get_pioneer_p3dx(client_id: int) -> int:
    robot_name = 'Pioneer_p3dx'
    mode = sim.simx_opmode_blocking

    _, pionner = sim.simxGetObjectHandle(client_id, robot_name, mode)

    assert pionner != -1, 'Não conseguiu achar o pionner'

    return pionner


def get_target(client_id: int) -> int:
    object_name = 'target'
    mode = sim.simx_opmode_blocking

    _, target = sim.simxGetObjectHandle(client_id, object_name, mode)

    assert target != -1, f'Não conseguiu achar o {object_name}'

    return target


def set_object_position(client_id: int, object_id: int, position: list[float]):
    sim.simxSetObjectPosition(client_id, object_id, -1, position, operationMode=sim.simx_opmode_blocking)


def send_path_4_drawing(path: list[float], client_id: int):
    """"    path é ou vetor de floats na seguinte ordem [x,y,z,x,y,z,x,y,z...]
            onde x,y,z é o valor da coordenada x,y,z de um ponto do caminho.
    """
    packed_data = sim.simxPackFloats(path)
    sim.simxWriteStringStream(client_id, "path_coord", packed_data, sim.simx_opmode_blocking)
