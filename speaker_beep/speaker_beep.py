import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from common_api.distance import DistanceReading
import numpy as np
from typing import List, Optional
from threading import Thread, Lock, Event
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

MIN_INTERVAL = 0.05
MAX_INTERVAL = 0.5

# Controls the shape of the exponential mapping. Values <1 make the curve rise
# faster at shorter distances (more aggressive), values >1 make it slower.
MAPPING_EXPONENT = 0.5

class SpeakerBeep():
    def __init__(self, debug: bool = False) -> None:
        self._debug: bool = debug
        self._closest_dist: Optional[float] = None
        self._curr_duration: Optional[float] = None
        self._audio_available: bool = SOUND_DEVICE_AVAILABLE

        # Thread controls.
        self._play_flag: Event = Event()
        self._thread: Optional[Thread] = None
        self._lock = Lock()
        
        # Cache the generated waveform so we don't need to recreate it on every beep call.
        t = np.linspace(0, BEEP_PLAY_DURATION, int(SAMP_RATE * BEEP_PLAY_DURATION), endpoint=False)
        self._cached_wave = 0.5 * np.sin(2 * np.pi * FREQ * t)
        
    def update_closest(self, nearby_objects: List[DistanceReading]) -> None:
        """Update with the closest valid distance reading, ignoring None readings."""
        if not nearby_objects:
            return
        
        # Filter out None readings before finding the closest
        valid_objects = [obj for obj in nearby_objects if obj.distance is not None]
        
        if not valid_objects:
            return
        
        # Find the closest valid object
        closest_object = min(valid_objects, key=lambda obj: obj.distance)
        self._closest_dist = closest_object.distance
        self._update_duration()

    def _map_dist_to_duration(self, distance: float) -> Optional[float]:
        # Normalize and clamp within [0, 1].
        norm = (distance - MIN_DIST) / (MAX_DIST - MIN_DIST)
        norm = max(0.0, min(norm, 1.0))
        
        duration = MIN_INTERVAL + (MAX_INTERVAL - MIN_INTERVAL) * (norm ** MAPPING_EXPONENT)
        return max(MIN_INTERVAL, min(MAX_INTERVAL, duration))
                
    def _update_duration(self) -> None:
        """Update beep interval based on current distance, handling None values."""
        if self._closest_dist is None:
            with self._lock:
                self._curr_duration = None
            return
    
        duration = self._map_dist_to_duration(self._closest_dist)
        with self._lock:
            self._curr_duration = duration

    def start(self):
        """Start the beeping loop once. Safe to call multiple times."""
        if self._thread and self._thread.is_alive():
            return
        self._play_flag.set()
        self._thread = Thread(target=self._beep_loop)
        self._thread.start()

    def _beep_loop(self):
        if self._debug:
            print("[DEBUG] Beep thread started.")
        while self._play_flag.is_set():
            with self._lock:
                dur = self._curr_duration
                dist = self._closest_dist

            # Busy wait if there is no current duration.
            if dur is None:
                time.sleep(0.1)
                
                if self._debug:
                    print(f"[DEBUG] Beeping (dist={dist}, dur={dur})")
                continue
            try:
                sd.play(self._cached_wave, SAMP_RATE)
                sd.wait()
            except Exception as e:
                if self._debug:
                    print(f"[DEBUG] Audio error: {e}")

            if self._debug:
                print(f"[DEBUG] Beeping (dist={dist:.1f}, dur={dur:.2f}s)")
            time.sleep(dur)
        
        if self._debug:
            print("[DEBUG] Beep thread exited.")

    def stop(self):
        """Signal the thread to stop and wait for it to exit."""
        if self._debug:
            print("[DEBUG] Stopping beep thread...")
        self._play_flag.clear()
        if self._thread:
            self._thread.join(timeout=1)
            self._thread = None
        try:
            if self._audio_available:
                sd.stop()
        except Exception as e:
            if self._debug:
                print(f"[DEBUG] Audio error: {e}")
