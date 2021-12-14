import dataclasses
import json
import os
from pathlib import Path

from modules.coppeliasim import coppeliasim
from modules.utils import Polygon, Vertex


def main():
    client_id = coppeliasim.try_to_connect_to_coppeliasim(port=19997)
    """me conectei na porta 19997 com a qual posso interagir com o simulador sem precisar iniciar a simulação"""

    obstacles_id = [f'obstacle_{index}' for index in range(1, 5)]

    """
            Obstáculo 1 possui 5 vertices
            Obstáculo 2 possui 3 vertices
            Obstáculo 3 possui 4 vertices
            Obstáculo 4 possui 5 vertices
    """
    total_of_vertices = [5, 3, 4, 5]

    obstacles = [create_obstacle(obstacles_id, total, client_id) for obstacles_id, total in
                 zip(obstacles_id, total_of_vertices)]

    robot_vertices = [create_vertex(name, client_id) for name in ["P1", "P2", "P3", "P4"]]

    robot = Polygon(name="Pioneer_p3dx", vertices=robot_vertices)

    """
    Por padrão estamos salvando qualquer dado que vem no simulador na pasta output raiz do repositório
    """
    output_path = Path('output')
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    to_json(obstacles + [robot], output_path.joinpath('obstacles_vertices.json'))


def create_obstacle(obstacle_name: str, total_vertices: int, client_id: int) -> Polygon:
    vertices = [create_vertex(f'{obstacle_name}_P{index}', client_id) for index in range(1, total_vertices + 1)]
    return Polygon(name=obstacle_name, vertices=vertices)


def create_vertex(vertex_name: str, client_id: int) -> Vertex:
    vertex_id = coppeliasim.get_object(client_id, vertex_name)
    position = coppeliasim.get_object_position(client_id, vertex_id)
    while position is None:
        position = coppeliasim.get_object_position(client_id, vertex_id)

    assert position is not None, "position não pode  vazio"
    pos_x_y = position[:2]
    return Vertex(name=vertex_name, position=pos_x_y)


def to_json(obstacles: list[Polygon], path_file: Path):
    dict_obstacles: list[dict] = [dataclasses.asdict(o) for o in obstacles]

    with open(path_file, 'w') as json_file:
        json_file.write(json.dumps(dict_obstacles))


if __name__ == '__main__':
    main()
