# Speaker Beep
This module is responsible for emitting a beep on the audio-jack connection of the RaspberryPi.

**Author:** Yihang Feng <br>
**Last Modified:** 10/01/2025

## Overview
The code implements the SpeakerBeep class to control to use `DistanceReading` objects containing distance information to nearby foreign objects relative to the 4 corners of the car. With these distances, it controls a beep emitted on the speaker.

### Strategy
The code implements the following functions:
- `update_closest` -> Identifies the nearest "threat" to the car based on distance detector readings.
- `update_duration` -> Maps a duration float value in sec for each iteration of the beep.
- `emit_beep` -> Plays the beep object on the speaker using sounddevice.
- `stop_beep` -> Stops any active beeping using sounddevice.