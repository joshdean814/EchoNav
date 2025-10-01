import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from common_api.angle import AngleReading
import numpy as np
from numpy.typing import NDArray
import glowbit

LED_DIM = 8

def check_angle(reading: AngleReading) -> None:
    """
    Validates an angle reading and passes it onwards.

    NOTE: we currently consider an angle is valid if it's in the range [-10°, 10°].

    Args:
        reading (AngleReading): the latest angle reading from the steering control.
    """
    if not reading.valid:
        return
    
    # TODO: Validate the angle is in the correct range.
    raise NotImplementedError()

def get_coords_from_angle(angle: float)-> NDArray:
    """
    Fills coordinates in a 2D numpy array (8x8). 
    
    If a light is "on", it is marked with a 1, else 0.

    Args:
        angle (float): current steering angle, in degrees.

    Returns:
        NDArray: 8x8 array containing pixel information.
    """

    # Start with a map of all zero values.
    coord_map = np.zeros(shape=(LED_DIM, LED_DIM))

    # TODO: use the angle to iterate to turn on correct pixel locations.
    raise NotImplementedError()

def draw_grid(coords: NDArray) -> None:
    """
    Uses glowbit to activate the Pi LED grid.

    Args:
        coords (NDArray): 8x8 array containing the illuminated coordinates.
    """

    # Initialize the 8x8 matrix.
    matrix = glowbit.matrix(8, 8)

    # Use red for active pixel colors.
    red = matrix.rgb_color(255, 0, 0)

    rows, cols = coords.shape
    for i in range(rows):
        for j in range(cols):
            # Check if coordinate is active.
            if coords[i, j]:
                # Activate pixel at coordinate.
                matrix.pixel_set(i, j, red)

    # Display the matrix.
    matrix.show()

def print_grid(coords: NDArray) -> None:
    """Debugging only method to visualize current matrix.
    
    Args:
        coords (NDArray): 8x8 array containing the illuminated coordinates.
    """
    for row in coords:
        print(" ".join("█" if cell else " " for cell in row))