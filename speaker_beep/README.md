# Speaker Beep
This module is responsible for emitting a beep on the audio-jack connection of the RaspberryPi.

**Author:** Yihang Feng <br>
**Date Modified:** 09/30/2025

## Overview
The code attempts to read `Collision` objects containing distance information to nearby foreign objects relative to the 4 corners of the car.

### Strategy
The code implements the following functions:
- `find_closest` -> Identifies the nearest "threat" to the car based on distance detector readings.
- `get_freq` -> Maps a distance float value to a frequency to be played on the speaker.
-`emit_beep` -> Plays the beep object on the speaker.