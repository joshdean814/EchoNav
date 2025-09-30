from ..common_api.distance import *
from typing import List

# Identifies the nearest "threat" to the car based on distance detector readings.
def find_closest(nearby_obj: List[Collision]) -> None:
    raise NotImplementedError()

# Plays the beep object on the speaker.
def emit_beep(closest_obj: Collision) -> None:
    raise NotImplementedError()

# Maps a distance float value to a frequency to be played on the speaker.
# TODO: figure out return type for this, some audio library object Raspberry pi accepts.
def get_freq(dist: float) -> ...:
    raise NotImplementedError()