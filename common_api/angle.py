from enum import IntEnum

class TurnState(IntEnum):
    LEFT_TURN   = -1
    IDLE        = 0
    RIGHT_TURN  = 1
    
    @property
    def name(self) -> str:
        name_map = {
            self.LEFT_TURN : "Left Turn",
            self.IDLE : "Idle",
            self.RIGHT_TURN : "Right Turn"
        }
        return name_map.get(self)
