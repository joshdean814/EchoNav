import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from common_api.distance import DistanceReading
import numpy as np
import sounddevice as sd
from typing import List, Optional
import time

SAMP_RATE = 44100          
FREQ = 1250.0
# How long to actually play the sinewave for each beep (seconds)
BEEP_PLAY_DURATION = 0.1

# Distance thresholds (in cm). Using named constants makes the mapping
# from distance -> beep interval easier to read and change.
CRITICAL_DISTANCE_CM = 10    # very close
WARNING_DISTANCE_CM = 30     # close
DANGER_DISTANCE_CM = 50      # alarm range upper bound

# Corresponding beep intervals (seconds) for the above ranges.
INTERVAL_CRITICAL = 0.5
INTERVAL_WARNING = 1.5
INTERVAL_DANGER = 3.0

# When outside alarm ranges, use this safe sleep interval between checks.
SAFE_SLEEP_INTERVAL = 1.0

class SpeakerBeep():
    def __init__(self) -> None:
        self._closest_dist: Optional[float] = None
        self._curr_duration: Optional[float] = None
        self._play_beep: bool = False

    def update_closest(self, nearby_objects: List[DistanceReading]) -> None:
        if not nearby_objects:
            self._closest_dist = None
            self._stop_beep()
            return
        
        closest_object = min(nearby_objects, key=lambda obj: obj.distance)
        self._closest_dist = closest_object.distance
        self._update_duration()
        

    def _update_duration(self):
        if self._closest_dist is None:
            self._curr_duration = None
            return
      
        # Map the closest distance to a readable, named interval.
        # Note: comparisons are exclusive of the lower bound (i.e. < CRITICAL_DISTANCE behaves as "very close").
        if self._closest_dist < CRITICAL_DISTANCE_CM:
            self._curr_duration = INTERVAL_CRITICAL
        elif self._closest_dist < WARNING_DISTANCE_CM:
            self._curr_duration = INTERVAL_WARNING
        elif self._closest_dist < DANGER_DISTANCE_CM:
            self._curr_duration = INTERVAL_DANGER
        else:
            # None indicates "no beeping" / safe distance
            self._curr_duration = None

    def play_beep(self) -> None:
        if not self._curr_duration or self._curr_duration <= 0.0:
            return

        try:
            # Only play a short tone regardless of the interval between beeps.
            t = np.linspace(0, BEEP_PLAY_DURATION, int(SAMP_RATE * BEEP_PLAY_DURATION), endpoint=False)
            wave = 0.5 * np.sin(2 * np.pi * FREQ * t)
            
            sd.play(wave, SAMP_RATE)
            
        except Exception as e:
            print(f"Audio error: {e}")

    def _stop_beep(self) -> None:
        self._play_beep = False
        try:
            sd.stop()
        except:
            pass

    def alarm_loop(self, get_distance_func):
        """
        Continuously beep while in alarm range.
        get_distance_func: a function that returns current distance (float or None)
        """
        print(f"Entering alarm loop. Will beep while distance < {DANGER_DISTANCE_CM}cm.")
        while True:
            dist = get_distance_func()
            # If no reading or we're outside the alarm region, stop.
            if dist is None or dist >= DANGER_DISTANCE_CM:
                print("Out of alarm range. Exiting alarm loop.")
                self._stop_beep()
                break
            self._closest_dist = dist
            self._update_duration()
            if self._curr_duration:
                self.play_beep()
                # Wait the configured interval between beeps.
                time.sleep(self._curr_duration)
            else:
                # No beeps in safe range: wait a short, constant amount before re-checking.
                time.sleep(SAFE_SLEEP_INTERVAL)