from typing import Protocol
from .grid_limits import GridLimits

import numpy as np


class Grid(Protocol):

    def limits(self) -> GridLimits:
        ...

    def get(self, x: int, y: int) -> np.ndarray:
        ...

    def is_valid_index(self, x: int, y: int) -> bool:
        ...
