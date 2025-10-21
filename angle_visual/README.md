# Angle Visual

This module handles the visual representation of the vehicle’s turn direction using the Sense HAT 8x8 LED matrix.

**Author:** Anju Damodaran <br>
**Last Modified:** 21/10/2025

# Overview

The AngleVisual class provides a simple interface between the turn state detection system and the Sense HAT LED display.
It visualizes the vehicle’s current steering direction by showing dynamic arrow patterns that point left, right, or down (idle/straight).

# Strategy

The module defines a set of pre-built arrow patterns represented as flattened 8×8 boolean matrices.
These are converted to red/black pixel maps and displayed on the Sense HAT using its built-in `set_pixels`.

# Arrows:

- `LEFT_TURN` -> displays a down-right arrow (mirrored perspective for reversing).
- `RIGHT_TURN` -> displays a down-left arrow.
- `IDLE` -> displays a downward arrow.

# Core Functions

- `display_arrow_from_turn` -> displays the corresponding arrow for a given TurnState.
- `_display_arrow` -> converts a binary arrow pattern into RGB pixel data and renders it on the LED grid.
- `clear_display` -> clears the LED matrix, turning off all pixels.