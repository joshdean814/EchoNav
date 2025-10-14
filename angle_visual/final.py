import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from common_api.angle import AngleReading
from sense_hat import SenseHat
import numpy as np
from numpy.typing import NDArray

LED_DIM = 8

# Initialize Sense HAT
sense = SenseHat()

# Colors
red = (255, 0, 0)
black = (0, 0, 0)

# Arrow definitions (8x8)
DOWN_ARROW = [
    black, black, black, red,   red,   black, black, black,
    black, black, black, red,   red,   black, black, black,
    black, black, black, red,   red,   black, black, black,
    black, black, black, red,   red,   black, black, black,
    red,   black, black, red,   red,   black, black, red,
    black, red,   black, red,   red,   black, red,   black,
    black, black, red,   red,   red,   red,   black, black,
    black, black, black, red,   red,   black, black, black
]

UP_RIGHT_ARROW = [
    black, black, black, black, red, red, red, red,
    black, black, black, black, black, black, red, red,
    black, black, black, black, black, red, black, red,
    black, black, black, black, red, black, black, red,
    black, black, black, red, black, black, black, black,
    black, black, red, black, black, black, black, black,
    black, red, black, black, black, black, black, black,
    red, black, black, black, black, black, black, black
]

UP_LEFT_ARROW = [
    red, red, red, red, black, black, black, black, 
    red, red, black, black, black, black, black, black,
    red, black, red, black, black, black, black, black,
    red, black, black, red, black, black, black, black,
    black, black, black, black, red, black, black, black,
    black, black, black, black, black, red, black, black,
    black, black, black, black, black, black, red, black,
    black, black, black, black, black, black, black, red
]

def check_angle(reading: AngleReading) -> float | None:
    """
    Validates an angle reading and returns it if valid.

    Args:
        reading (AngleReading): the latest angle reading.

    Returns:
        float | None: The valid angle or None if invalid.
    """
    if not reading.valid:
        return None
    if -10 <= reading.value <= 10:
        return reading.value
    return None

def display_arrow(angle: float) -> None:
    """
    Displays the correct arrow on the Sense HAT based on angle.

    Args:
        angle (float): Current steering angle in degrees.
    """
    if angle < 0:
        sense.set_pixels(UP_LEFT_ARROW)
    elif angle == 0:
        sense.set_pixels(DOWN_ARROW)
    elif angle > 0:
        sense.set_pixels(UP_RIGHT_ARROW)
    else:
        sense.clear()

# Optional: Convert angle to 8x8 grid (for debugging / extension)
def get_coords_from_angle(angle: float) -> NDArray:
    """
    Creates an 8x8 grid with a single active pixel representing the angle.

    Args:
        angle (float): Steering angle in degrees.

    Returns:
        NDArray: 8x8 array of 0s and 1s.
    """
    coord_map = np.zeros((LED_DIM, LED_DIM))
    # Map angle -10..10 to column 0..7
    col = int(np.clip((angle + 10) / 20 * (LED_DIM - 1), 0, LED_DIM - 1))
    row = LED_DIM // 2  # Middle row
    coord_map[row, col] = 1
    return coord_map

def draw_grid(coords: NDArray) -> None:
    """Displays the 8x8 array on Sense HAT."""
    pixels = []
    for row in coords:
        for cell in row:
            pixels.append(red if cell else black)
    sense.set_pixels(pixels)

# Example usage
if __name__ == "__main__":
    # Example angle reading

        display_arrow(0)
        # Optional: also show grid version
        # draw_grid(get_coords_from_angle(angle))

