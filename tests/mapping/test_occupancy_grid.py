import unittest

from src.modules.grid import OccupancyGrid, GridLimits


class OccupancyGridTestCase(unittest.TestCase):

    def test_access_grid(self):

        limits = GridLimits(x_min=0, x_max=10, y_min=0, y_max=10, resolution=1)

        grid = OccupancyGrid(limits)

        value = grid.get(0, 0)

        self.assertEquals(value, 0, msg="Todas as células devem começar com log-odd igual a 0")

        grid.set_log_odd(8, 8, 10)

        self.assertEquals(grid.get(8, 8), 10, msg="deve-se ser capaz de atualizar o grid")

        grid_width_x = int(round((limits.x_max - limits.x_min) / limits.resolution))
        grid_width_y = int(round((limits.y_max - limits.y_min) / limits.resolution))

        with self.assertRaises(IndexError):
            grid.set_log_odd(-1, 0, value=10)

        with self.assertRaises(IndexError):
            grid.set_log_odd(grid_width_x-1, 0, value=10)

        with self.assertRaises(IndexError):
            grid.set_log_odd(0, grid_width_y-1, value=10)

        for x_index in range(grid_width_x-1):
            for y_index in range(grid_width_y-1):
                grid.get(x_index, y_index)
                grid.set_log_odd(x_index, y_index, 19)

    def test_valid_index(self):
        limits = GridLimits(x_min=0, x_max=10, y_min=0, y_max=10, resolution=1)

        grid = OccupancyGrid(limits)

        self.assertTrue(grid.is_valid_index(0, 0))
        self.assertFalse(grid.is_valid_index(-1, 0))
        self.assertFalse(grid.is_valid_index(0, -1))

        self.assertFalse(grid.is_valid_index(0, limits.y_max))
        self.assertFalse(grid.is_valid_index(limits.x_max, 0))
