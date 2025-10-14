from enum import IntEnum
from typing import Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

class CarCorner(IntEnum):
    BACK_LEFT = 0
    BACK_RIGHT = 1
    #FRONT_LEFT = 2
    #FRONT_RIGHT = 3
    
    @property
    def print_name(self) -> str:
        return self.name.replace("_", " ").lower().title()
    
    @property
    def pins(self) -> Tuple[int]:
        pin_map = {
            self.BACK_RIGHT : (17, 27),
            self.BACK_LEFT : (16, 26)
        }
        return pin_map.get(self)
    
@dataclass
class DistanceReading:
    corner: CarCorner
    distance: Optional[float]
