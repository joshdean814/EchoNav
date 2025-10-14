from enum import IntEnum
from typing import Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

class CarCorner(IntEnum):
    BACK_RIGHT = 0
    BACK_LEFT = 1
    #FRONT_LEFT = 2
    #FRONT_RIGHT = 3
    
    @property
    def print_name(self) -> str:
        return self.name.replace("_", " ").lower().title()
    
    @property
    def pins(self) -> Tuple[int]:
        pin_map = {
            self.BACK_RIGHT : (17, 27),
            self.BACK_LEFT : (23, 24)
        }
        return pin_map.get(self)
    
@dataclass
class DistanceReading:
    corner: CarCorner
    distance: Optional[float]
    timestamp: datetime = field(default_factory=datetime.now)
