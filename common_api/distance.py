from enum import IntEnum
from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime

class CarCorner(IntEnum):
    BACK_LEFT = 1
    BACK_RIGHT = 2
    FRONT_LEFT = 3
    FRONT_RIGHT = 4

@dataclass
class DistanceReading:
    corner: CarCorner
    distance: Optional[float]
    timestamp: datetime = field(default_factory=datetime.now)