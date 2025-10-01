import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from common_api.distance import Collision
import numpy as np
import sounddevice as sd
from typing import List, Optional

# Fixed sample rate and frequency for simplicity.
SAMP_RATE = 44100          
FREQ = 1250.0

class SpeakerBeep():
    """Class for controlling the speaker's beeping output based on distance readings."""

    def __init__(self) -> None:
        """
        Sets up SpeakerBeep class members.

        Members:
            _closest_dist (float | None): nearmost threat object, or None if car is safe.
            _curr_duration (float | None): closest object distance, or None if car is safe.
            _play_beep (bool): False if beep is off, else True.
        """
        
        self._closest_dist: Optional[float] = None
        self._curr_duration: Optional[float] = None
        self._play_beep: bool = False

    def update_closest(self, nearby_objects: List[Collision]) -> None:
        """Identifies the nearest "threat" to the car based on distance detector readings.

        Then triggers a beep sound on that object. If no object is found, kills the current beep.
        
        Args:
            nearby_objects (Collision): Detected objects on the four corners of the car.
        """
        # TODO: Iterate the list of collisions and only act on the closest, or kill beep and exit.
        # NOTE: If the nearest distance has not changed, exit.
        raise NotImplementedError()

    def update_duration(self):
        """Maps a duration float value in sec for each iteration of the beep.
        
        Returns:
            float: seconds each beep sound should last, in range (0, 100].
        """
        if self._closest_dist == 0.0:
            return
        
        # TODO: figure out the relationship between obj distance and beep duration.
        # Set self._curr_duration with the result.
        raise NotImplementedError()

    def emit_beep(self, closest: Collision) -> None:
        """
        Plays the beep object on the speaker using sounddevice.

        Calls `get_duration` to get deep length information.

        NOTE: `stop_beep` should be called before this.

        Args:
            closest (Collision): the nearest object to warn about. 
        """

        if not self._curr_duration or self._curr_duration <= 0.0:
            raise RuntimeError("Invalid beep duration!")

        t = np.linspace(0, self._curr_duration, int(SAMP_RATE * self._curr_duration), endpoint=False)
        wave = 0.5 * np.sin(2 * np.pi * FREQ * t)

        self._play_beep = True

        while self._play_beep:
            sd.play(wave, SAMP_RATE)
            sd.wait()

    def stop_beep(self) -> None:
        """Stops any active beeping using sounddevice."""
        self._play_beep = False
        sd.stop()