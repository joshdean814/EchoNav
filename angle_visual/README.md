# Angle Visual
This module is responsible for displaying the current steering vector.

**Author:** Anju Damodaran \\
**Date Modified:** 09/30/2025

## Overview
The code attempts to read `AngleReading` objects and map valid angles to a vector displayed on the RaspberryPi's 8x8 LED interface. It expects an input angle in the range of [-10°, 10], where 0° is centered, -10° is all the way left, and 10° is all the way right.

### Strategy
The code implements the following functions:
- `check_angle` -> Validates provided `AngleReading`.
- `map_angle_to_coords` -> uses the angle to create a 2D, 8x8 numpy array containing the current vector data.
- `create_grid` -> Creates a Pillow grid object using the pixel data.
- `draw_grid` -> Draws the actual grid on the Python LED interface.