from enum import IntEnum
from typing import Optional

class CarCorner(IntEnum):
    BACK_LEFT = 1
    BACK_RIGHT = 2
    FRONT_LEFT = 3
    FRONT_RIGHT = 4

class Collision:
    corner: CarCorner
    distance: Optional[float]