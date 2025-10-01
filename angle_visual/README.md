# Angle Visual
This module is responsible for displaying the current steering vector.

**Author:** Anju Damodaran <br>
**Date Modified:** 10/01/2025

## Overview
The code attempts to read `AngleReading` objects and map valid angles to a vector displayed on the RaspberryPi's 8x8 LED interface. It expects an input angle in the range of [-10°, 10], where 0° is centered, -10° is all the way left, and 10° is all the way right.

### Strategy
The code implements the following functions:
- `check_angle` -> Validates provided `AngleReading` & passes it forwards.
- `get_coords_from_angle` -> uses the angle to create a 2D, 8x8 numpy array containing the current pixel data.
- `draw_grid` -> Uses glowbit to activate the Pi LED grid using coordinate information.