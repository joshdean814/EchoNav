import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from common_api.distance import DistanceReading
import numpy as np
from typing import List, Optional
import threading
import time

# Try to import sounddevice, but have a fallback
try:
    import sounddevice as sd
    SOUND_DEVICE_AVAILABLE = True
    sd.default.device = [-1, 1]
    print("INFO: sounddevice library is available")
except ImportError:
    SOUND_DEVICE_AVAILABLE = False
    print("WARNING: sounddevice library not available. Using fallback audio method.")

SAMP_RATE = 44100          
FREQ = 1250.0
BEEP_PLAY_DURATION = 0.05

# Distance thresholds (in cm). Using named constants makes the mapping
# from distance -> beep interval easier to read and change.
MAX_DIST = 50   # alarm range upper bound
MIN_DIST = 2    # very close

# Controls the shape of the exponential mapping. Values <1 make the curve rise
# faster at shorter distances (more aggressive), values >1 make it slower.
MAPPING_EXPONENT = 0.5

class SpeakerBeep():
    def __init__(self, debug: bool = False) -> None:
        self._debug: bool = debug
        self._closest_dist: Optional[float] = None
        self._curr_duration: Optional[float] = None
        self._audio_available: bool = SOUND_DEVICE_AVAILABLE
        self._beep_thread: threading.Thread = None
        self._play_flag: threading.Event = threading.Event()
        
        # Cache the generated waveform so we don't need to recreate it on every beep call.
        self._cached_wave = None
        
        if not self._audio_available:
            print("WARNING: Audio playback disabled. SpeakerBeep will only print beep messages.")

    def update_closest(self, nearby_objects: List[DistanceReading]) -> None:
        """Update with the closest valid distance reading, ignoring None readings."""
        if not nearby_objects:
            self._closest_dist = None
            self.stop_beep()
            return
        
        # Filter out None readings before finding the closest
        valid_objects = [obj for obj in nearby_objects if obj.distance is not None]
        
        if not valid_objects:
            # All readings are None - treat as no objects
            self._closest_dist = None
            self.stop_beep()
            return
        
        # Find the closest valid object
        closest_object = min(valid_objects, key=lambda obj: obj.distance)
        self._closest_dist = closest_object.distance
        if self._update_duration():
            self.play_beep()

    def _map_dist_to_duration(self, distance: float) -> Optional[float]:
        if distance >= MAX_DIST:
            return
        
        if distance <= MIN_DIST:
            return 0.05
        
        norm = (distance - MIN_DIST) / (MAX_DIST - MIN_DIST)
        duration = MIN_DIST + (MAX_DIST - MIN_DIST) * (norm ** MAPPING_EXPONENT)
        return duration
                
    def _update_duration(self) -> bool:
        """Update beep interval based on current distance, handling None values."""
        if self._closest_dist is None:
            self._curr_duration = None
            return
       
        if duration := self._map_dist_to_duration(self._closest_dist):
            self._curr_duration = duration

        return self._curr_duration is not None

    def stop_beep(self):
        if self._debug:
            print("[DEBUG] Attempting to stop beeping...")
    
        self._play_flag.clear()
        try:
            if self._audio_available:
                sd.stop()
        
        except:
            if self._debug:
                print("[DEBUG] Failed to stop beeping!")
        if self._debug:
            print("[DEBUG] Clearing beep thread, cached wave...")
        
        if self._beep_thread:
            self._beep_thread.join()
            
        self._cached_wave = None
        
        if self._debug:
            print("[DEBUG] Beeping stopped.")

    def play_beep(self):
        
        # Last sanity check before playing the beep.
        if not self._curr_duration or self._curr_duration <= 0.0:
            self.stop_beep()
            return

        self._play_flag.set()

        def _loop():
            while self._play_flag.is_set():
                if self._audio_available:
                    if self._cached_wave is None:
                        t = np.linspace(0, BEEP_PLAY_DURATION, int(SAMP_RATE * BEEP_PLAY_DURATION), endpoint=False)
                        self._cached_wave = 0.5 * np.sin(2 * np.pi * FREQ * t)
                    sd.play(self._cached_wave, SAMP_RATE)
                if self._debug:
                    print(f"[DEBUG] Beep with distance: {self._closest_dist}cm, interval: {self._curr_duration}s")
                time.sleep(self._curr_duration)

        self._beep_thread = threading.Thread(target=_loop)
        self._beep_thread.start()
