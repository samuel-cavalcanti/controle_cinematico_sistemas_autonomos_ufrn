from dataclasses import dataclass


@dataclass
class GridLimits:
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    resolution: float
