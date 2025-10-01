import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from common_api.distance import DistanceReading
import numpy as np
import sounddevice as sd
from typing import List, Optional

SAMP_RATE = 44100          
FREQ = 1250.0

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
      
        if self._closest_dist < 10:      
            self._curr_duration = 0.5    
        elif self._closest_dist < 30:    
            self._curr_duration = 1.5
        elif self._closest_dist < 50:    
            self._curr_duration = 3.0
        else:                            
            self._curr_duration = None

    def play_beep(self) -> None:
        if not self._curr_duration or self._curr_duration <= 0.0:
            return

        try:
            beep_duration = 0.1
            t = np.linspace(0, beep_duration, int(SAMP_RATE * beep_duration), endpoint=False)
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