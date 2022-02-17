from enum import Enum, auto
class Space(Enum):
    free = auto()
    occupied = auto()
    out_of_range = auto()