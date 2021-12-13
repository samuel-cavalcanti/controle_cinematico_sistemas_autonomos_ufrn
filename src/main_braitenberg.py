from modules import coppeliasim, controllers


def main():
    client_id = coppeliasim.try_to_connect_to_coppeliasim(port=19999)

    left_motor, right_motor = coppeliasim.get_motors(client_id)

    proximity_sensors = coppeliasim.get_sensors(client_id)

    while coppeliasim.simulation_is_alive(client_id):

        distances = coppeliasim.read_sensors(client_id, proximity_sensors)

        if distances:
            pioneer_velocity = controllers.braitenberg_controller(distances)

            coppeliasim.set_motor_velocity(client_id, left_motor, pioneer_velocity.left)
            coppeliasim.set_motor_velocity(client_id, right_motor, pioneer_velocity.right)


if __name__ == '__main__':
    main()
