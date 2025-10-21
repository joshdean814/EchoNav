"""This module creates an interface for the AngleCapture and Angle Visual modules.

File: angle.py
Author: Josh Dean
Last Modified: 21/10/2025
"""
from enum import IntEnum

class TurnState(IntEnum):
    """Represents the current turning state of the vehicle.

    Three possible states:
    - LEFT_TURN -> The vehicle is turning left.
    - IDLE -> The vehicle is stationary or moving straight.
    - RIGHT_TURN -> The vehicle is turning right.
    """
    LEFT_TURN   = -1
    IDLE        = 0
    RIGHT_TURN  = 1
    
    @property
    def name(self) -> str:
        """Returns a user-friendly name for the current turn state."""
        name_map = {
            self.LEFT_TURN : "Left Turn",
            self.IDLE : "Idle",
            self.RIGHT_TURN : "Right Turn"
        }
        return name_map.get(self)
