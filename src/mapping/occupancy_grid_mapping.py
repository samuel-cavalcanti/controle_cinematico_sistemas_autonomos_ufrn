from ..grid import Grid

import numpy as np
class OccupancyGridMapping:

    __occupancy_grid: Grid

    def __init__(self, occupancy_grid: Grid) -> None:
        self.__occupancy_grid = occupancy_grid

    def one_it(self, robot_state):

        limits = self.__occupancy_grid.limits()

        grid_width_x = int(round((limits.x_max - limits.x_min) / limits.resolution))
        grid_width_y = int(round((limits.y_max - limits.y_min) / limits.resolution))

        x_space = np.linspace(limits.x_min, limits.x_max, grid_width_x)
        y_space = np.linspace(limits.y_min, limits.y_max, grid_width_y)

        for x_index, x_cell in enumerate(x_space):
            for y_index,y_cell in enumerate(y_space):
                pass
                

    def in_perceptual_field(self, cell, robot_state) -> bool:
        pass

    def inverse_sensor_model(self, cell, x_t, z_t) -> float:
        pass


"""
1. coletar x,y, theta de todos os sensores e armazenar isso em um JSON
2.

"""