import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from common_api.angle import AngleReading
from sense_hat import SenseHat
import numpy as np
from numpy.typing import NDArray
from time import sleep
from enum import IntEnum

LED_DIM = 8

# Initialize Sense HAT
sense = SenseHat()

# Colors
red = (255, 0, 0)
black = (0, 0, 0)

# class ArrowState(IntEnum):
#     DOWN_LEFT_ARROW =   -1
#     DOWN_ARROW =        0
#     DOWN_RIGHT_ARROW =  1
    

# Arrow definitions (8x8 flattened lists of 0s and 1s)
DOWN_ARROW = [
    0, 0, 0, 1, 1, 0, 0, 0,
    0, 0, 0, 1, 1, 0, 0, 0,
    0, 0, 0, 1, 1, 0, 0, 0,
    0, 0, 0, 1, 1, 0, 0, 0,
    1, 0, 0, 1, 1, 0, 0, 1,
    0, 1, 0, 1, 1, 0, 1, 0,
    0, 0, 1, 1, 1, 1, 0, 0,
    0, 0, 0, 1, 1, 0, 0, 0
]

DOWN_RIGHT_ARROW = [
    0, 0, 0, 0, 1, 1, 1, 1,
    0, 0, 0, 0, 0, 0, 1, 1,
    0, 0, 0, 0, 0, 1, 0, 1,
    0, 0, 0, 0, 1, 0, 0, 1,
    0, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 0,
    1, 0, 0, 0, 0, 0, 0, 0
]

DOWN_LEFT_ARROW = [
    1, 1, 1, 1, 0, 0, 0, 0,
    1, 1, 0, 0, 0, 0, 0, 0,
    1, 0, 1, 0, 0, 0, 0, 0,
    1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 0, 0,
    0, 0, 0, 0, 0, 1, 0, 0,
    0, 0, 0, 0, 0, 0, 1, 0,
    0, 0, 0, 0, 0, 0, 0, 1
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

def display_arrow(angle: float, arrow_pattern: list) -> None:
    """
    Displays the arrow pattern on the Sense HAT.

    Args:
        angle (float): Current steering angle in degrees (for selection).
        arrow_pattern (list): Flattened 8x8 list of 0s and 1s for the arrow.
    """
    pixels = []
    for cell in arrow_pattern:
        pixels.append(red if cell == 1 else black)
    sense.set_pixels(pixels)

def display_arrow_from_angle(angle: float) -> None:
    """
    Selects and displays the correct arrow based on angle.

    Args:
        angle (float): Current steering angle in degrees.
    """
    if angle < 0:
        display_arrow(angle, DOWN_LEFT_ARROW)
    elif angle == 0:
        display_arrow(angle, DOWN_ARROW)
    elif angle > 0:
        display_arrow(angle, DOWN_RIGHT_ARROW)
    else:
        sense.clear()

def display_arrow_from_reading(reading: AngleReading) -> None:
    """
    Validates and displays the arrow based on an AngleReading.

    Args:
        reading (AngleReading): The latest angle reading.
    """
    validated_angle = check_angle(reading)
    if validated_angle is not None:
        display_arrow_from_angle(validated_angle)
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
            pixels.append(red if cell == 1 else black)
    sense.set_pixels(pixels)

# Example usage / Driver simulation
if __name__ == "__main__":
    # Test cases
    test_angles = [-10, -5, 0, 5, 10, 15]  # 15 should be invalid (>10)
    
    for test_value in test_angles:
        # Create simulated reading
        reading = AngleReading(value=test_value, valid=True)
        
        # Use the integrated function
        display_arrow_from_reading(reading)
        
        # Optional: also show grid version
        validated_angle = check_angle(reading)
        if validated_angle is not None:
            draw_grid(get_coords_from_angle(validated_angle))
        
        sleep(2)  # Pause to see each display
    
    # Clear at end
    sense.clear()
