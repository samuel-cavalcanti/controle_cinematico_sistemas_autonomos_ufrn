import controllers
import coppeliasim
import utils
from path_planning import path_by_polynomials
from utils import Position


def draw_path(client_id: int, initial_pos: Position, final_pos: Position):
    x_coefficients, y_coefficients = path_by_polynomials.find_coefficients(initial_pos, final_pos)
    p_x, p_y, theta_t = path_by_polynomials.create_path_functions(x_coefficients, y_coefficients)

    path_points = path_by_polynomials.path_points_generator(p_x, p_y)

    coppeliasim.send_path_4_drawing(path_points, client_id)


def main():
    client_id = coppeliasim.connect_to_coppelia_sim(port=19999)

    left_motor, right_motor = coppeliasim.get_motors(client_id)

    proximity_sensors = coppeliasim.get_sensors(client_id)

    initial = utils.Position(x=-1.2945, y=0.050001, theta_in_rads=0)
    final = utils.Position(2.1, 2.1, utils.deg2rad(45))

    draw_path(client_id, initial_pos=initial, final_pos=final)

    while coppeliasim.simulation_is_alive(client_id):

        distances = coppeliasim.read_sensors(client_id, proximity_sensors)

        if distances:
            pioneer_velocity = controllers.braitenberg_controller(distances)

            coppeliasim.set_motor_velocity(client_id, left_motor, pioneer_velocity.left)
            coppeliasim.set_motor_velocity(client_id, right_motor, pioneer_velocity.right)


if __name__ == '__main__':
    main()
