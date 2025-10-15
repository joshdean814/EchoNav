import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from common_api.angle import TurnState
from sense_hat import SenseHat
from typing import List

# Colors options.
RED     = (255, 0, 0)
BLACK   = (0, 0, 0)

# Arrow definitions (8x8 flattened lists of 0s and 1s).
DOWN_ARROW: List[bool] = [
    0, 0, 0, 1, 1, 0, 0, 0,
    0, 0, 1, 1, 1, 1, 0, 0,
    0, 1, 0, 1, 1, 0, 1, 0,
    0, 0, 0, 1, 1, 0, 0, 0,
    1, 0, 0, 1, 1, 0, 0, 1,
    0, 0, 0, 1, 1, 0, 0, 0,
    0, 0, 0, 1, 1, 0, 0, 0,
    0, 0, 0, 1, 1, 0, 0, 0
]

DOWN_RIGHT_ARROW: List[bool] = [
    0, 0, 0, 0, 1, 1, 1, 1,
    0, 0, 0, 0, 0, 0, 1, 1,
    0, 0, 0, 0, 0, 1, 0, 1,
    0, 0, 0, 0, 1, 0, 0, 1,
    0, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 0,
    1, 0, 0, 0, 0, 0, 0, 0
]

DOWN_LEFT_ARROW: List[bool] = [
    1, 1, 1, 1, 0, 0, 0, 0,
    1, 1, 0, 0, 0, 0, 0, 0,
    1, 0, 1, 0, 0, 0, 0, 0,
    1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 0, 0,
    0, 0, 0, 0, 0, 1, 0, 0,
    0, 0, 0, 0, 0, 0, 1, 0,
    0, 0, 0, 0, 0, 0, 0, 1
]

class AngleVisual():
    def __init__(self) -> None:
        # Initialize Sense HAT
        self._sense = SenseHat()
        self.clear_display()
    
    def clear_display(self) -> None:
        self._sense.clear()

    def _display_arrow(self, arrow_pattern: List[bool]) -> None:
        """
        Displays the arrow pattern on the Sense HAT.

        Args:
            angle (float): Current steering angle in degrees (for selection).
            arrow_pattern (list): Flattened 8x8 list of 0s and 1s for the arrow.
        """
        pixels = []
        for cell in arrow_pattern:
            pixels.append(RED if cell else BLACK)
        self._sense.set_pixels(pixels)

    def display_arrow_from_turn(self, turn: TurnState) -> None:
        # NOTE: use reverse mappings, as the car is going backwards.
        arrow_map = {
            TurnState.LEFT_TURN : DOWN_RIGHT_ARROW,
            TurnState.IDLE : DOWN_ARROW,
            TurnState.RIGHT_TURN : DOWN_LEFT_ARROW
        }
        self._display_arrow(arrow_map.get(turn))
