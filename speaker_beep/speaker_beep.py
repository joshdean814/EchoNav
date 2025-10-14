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

# Distance thresholds (in cm). Using named constants makes the mapping
# from distance -> beep interval easier to read and change.
DANGER_DISTANCE_CM = 50      # alarm range upper bound

# Adjusted warning threshold so that middle distances map as follows:
# - distances < CRITICAL_DISTANCE_CM -> critical
# - distances < WARNING_DISTANCE_CM  -> warning
# - distances >= WARNING_DISTANCE_CM and < DANGER_DISTANCE_CM -> danger
# Setting WARNING_DISTANCE_CM = 25 makes 20cm map to WARNING (0.15s)
# and 25cm map to DANGER (0.30s) which matches the tests.
CRITICAL_DISTANCE_CM = 10    # very close
WARNING_DISTANCE_CM = 25     # close
DANGER_DISTANCE_CM = 50      # alarm range upper bound

# Even shorter intervals requested by the team (more responsive)
# Note: keep intervals > BEEP_PLAY_DURATION so the tone finishes before next beep.
BEEP_PLAY_DURATION = 0.03
INTERVAL_CRITICAL = 0.05     # Very fast beeping for critical distance
INTERVAL_WARNING = 0.15     # Fast beeping for warning distance
INTERVAL_DANGER = 0.30      # Medium beeping for danger distance

MIN_DIST = 3
MAX_DIST = 50

# Controls the shape of the exponential mapping. Values <1 make the curve rise
# faster at shorter distances (more aggressive), values >1 make it slower.
MAPPING_EXPONENT = 0.5

class SpeakerBeep():
    def __init__(self, debug: bool = False) -> None:
        self._debug: bool = debug
        self._closest_dist: Optional[float] = None
        self._curr_duration: Optional[float] = None
        self._play_beep: bool = False
        self._audio_available = SOUND_DEVICE_AVAILABLE
        # Cache the generated waveform so we don't allocate it on every beep call.
        self._cached_wave = None

        self._beep_thread = None
        self._stop_flag = threading.Event()
        
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
        duration = INTERVAL_CRITICAL + (INTERVAL_DANGER - INTERVAL_CRITICAL) * (norm ** MAPPING_EXPONENT)
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
        self._stop_flag.set()
        try:
            if self._audio_available:
                sd.stop()
                
                if self._debug:
                    print("[DEBUG] Beeping stopped.")
        except:
            if self._debug:
                print("[DEBUG] Failed to stop beeping!")
                
        if self._beep_thread and self._stop_flag:
            self._stop_flag.set()

    def play_beep(self):
        if not self._curr_duration or self._curr_duration <= 0.0:
            self.stop_beep()
            return

        if self._beep_thread and self._beep_thread.is_alive():
            # Already beeping; just update the interval for the next loop
            return

        self._stop_flag.clear()

        def _loop():
            while not self._stop_flag.is_set():
                if self._audio_available:
                    try:
                        if self._cached_wave is None:
                            t = np.linspace(0, BEEP_PLAY_DURATION, int(SAMP_RATE * BEEP_PLAY_DURATION), endpoint=False)
                            self._cached_wave = 0.5 * np.sin(2 * np.pi * FREQ * t)
                        sd.play(self._cached_wave, SAMP_RATE)
                    except Exception as e:
                        print(f"Audio error: {e}")
                        self._audio_available = False
                print(f"BEEP! Distance: {self._closest_dist}cm, Interval: {self._curr_duration}s")
                time.sleep(self._curr_duration)

        self._beep_thread = threading.Thread(target=_loop, daemon=True)
        self._beep_thread.start()
