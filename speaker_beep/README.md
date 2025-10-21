# Speaker Beep

This module is responsible for generating audio feedback through the Raspberry Pi’s audio jack. It produces periodic beeps whose frequency varies according to the proximity of detected obstacles.

**Author:** Yihang Feng <br>
**Last Modified:** 21/10/2025

## Overview

The code implements the `SpeakerBeep` class, which uses `DistanceReading` objects to determine the closest detected obstacle around the vehicle. Based on the measured distance, the module adjusts the interval between beeps to give intuitive auditory feedback.


## Strategy

The module performs the following key tasks:

- Initializes a continuous beep waveform and prepares a background thread to manage playback.
- Dynamically adjusts beep intervals based on distance values using an exponential mapping curve.
- Provides continuous feedback until stopped or distance updates are no longer available.

## Core Functions

- `update_closest` -> Processes a list of DistanceReading objects and identifies the nearest valid distance.
- `_map_dist_to_duration` -> Converts a distance value (in cm) to a beeping interval (in seconds).
- `_beep_loop` -> Runs a threaded loop to continuously play and space out beeps based on the current interval.
- `start` -> Starts the background beeping thread if not already running.

## Testing

The module also utilized two testing files `test_speaker.py` and `test_speaker2.py` to roughly validate module behavior.