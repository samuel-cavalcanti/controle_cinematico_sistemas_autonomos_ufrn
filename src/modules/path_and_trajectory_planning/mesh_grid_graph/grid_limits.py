from dataclasses import dataclass


@dataclass
class GridLimits:
    x_limits: tuple[float, float]
    y_limits: tuple[float, float]
