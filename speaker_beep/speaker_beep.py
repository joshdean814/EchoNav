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

MIN_DIST = 2
MAX_DIST = 50

# If True, use continuous exponential mapping between critical and danger
# instead of discrete buckets. This makes the interval grow smoothly with distance.
USE_CONTINUOUS_MAPPING = True
# Controls the shape of the exponential mapping. Values <1 make the curve rise
# faster at shorter distances (more aggressive), values >1 make it slower.
MAPPING_EXPONENT = 0.25

# When outside alarm ranges, use this safe sleep interval between checks.
SAFE_SLEEP_INTERVAL = 1.0

class SpeakerBeep():
    def __init__(self) -> None:
        self._closest_dist: Optional[float] = None
        self._curr_duration: Optional[float] = None
        self._play_beep: bool = False
        self._audio_available = SOUND_DEVICE_AVAILABLE
        # Cache the generated waveform so we don't allocate it on every beep call.
        self._cached_wave = None
        
        if not self._audio_available:
            print("WARNING: Audio playback disabled. SpeakerBeep will only print beep messages.")

    def update_closest(self, nearby_objects: List[DistanceReading], play: bool = True) -> None:
        """Update with the closest valid distance reading, ignoring None readings.

        If `play` is True and a valid interval is determined, `play_beep()` will be
        invoked immediately (non-blocking). Default is False to preserve existing behavior.
        """
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
        self._update_duration()

        # Optionally trigger an immediate beep (non-blocking). This keeps
        # existing callers unchanged (play=False) while allowing callers that
        # expect immediate feedback to request it.
        if play and self._curr_duration:
            self.play_beep()

    def _map_dist_to_duration(self, distance: float) -> Optional[float]:
        if distance >= MAX_DIST or distance <= MIN_DIST:
            return None
        
        duration = 1 / (0.1 * (distance - 2))
        return duration
        
    def _update_duration(self):
        """Update beep interval based on current distance, handling None values."""
        if self._closest_dist is None:
            self._curr_duration = None
            return
        # Optionally use a continuous exponential mapping from distance to interval.
        # This maps distances in [CRITICAL_DISTANCE_CM, DANGER_DISTANCE_CM) to
        # intervals between INTERVAL_CRITICAL and INTERVAL_DANGER.
        if USE_CONTINUOUS_MAPPING:
            # if self._closest_dist < CRITICAL_DISTANCE_CM:
            #     self._curr_duration = INTERVAL_CRITICAL
            # elif self._closest_dist >= DANGER_DISTANCE_CM:
            #     self._curr_duration = None
            # else:
            #     # normalized in [0,1] across the warning->danger span
            #     norm = (self._closest_dist - CRITICAL_DISTANCE_CM) / max(1.0, (DANGER_DISTANCE_CM - CRITICAL_DISTANCE_CM))
            #     # exponential interpolation with adjustable exponent to control
            #     # how quickly the interval grows with distance.
            #     # Apply exponent to norm to adjust curve steepness.
            #     adj = norm ** MAPPING_EXPONENT
            #     ratio = (INTERVAL_DANGER / INTERVAL_CRITICAL) ** adj
            #     self._curr_duration = INTERVAL_CRITICAL * ratio
            if duration := self._map_dist_to_duration(self._closest_dist):
                self._curr_duration = duration
        else:
            # Map the closest distance to discrete buckets (legacy behavior)
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
        """Play a beep if we have a valid distance and interval."""
        if not self._curr_duration or self._curr_duration <= 0.0:
            return

        try:
            # Only play a short tone regardless of the interval between beeps.
            # Cache the wave so repeated beeps are fast.
            if self._cached_wave is None:
                t = np.linspace(0, BEEP_PLAY_DURATION, int(SAMP_RATE * BEEP_PLAY_DURATION), endpoint=False)
                self._cached_wave = 0.5 * np.sin(2 * np.pi * FREQ * t)

            if self._audio_available:
                # Play in a short-lived background thread to ensure this method returns quickly.
                def _play(wave_buf):
                    try:
                        sd.play(wave_buf, SAMP_RATE)
                    except Exception as e:
                        print(f"Audio error in thread: {e}")

                thr = threading.Thread(target=_play, args=(self._cached_wave,), daemon=True)
                thr.start()
                print(f"BEEP! Distance: {self._closest_dist}cm, Interval: {self._curr_duration}s")
            else:
                # Fallback: just print a message (quick)
                print(f"BEEP! (Audio disabled) Distance: {self._closest_dist}cm, Interval: {self._curr_duration}s")
            
        except Exception as e:
            print(f"Audio error: {e}")
            # Disable audio on error to prevent repeated error messages
            self._audio_available = False

    def stop_beep(self) -> None:
        """Stop any ongoing audio playback."""
        self._play_beep = False
        try:
            if self._audio_available:
                sd.stop()
        except:
            pass

    # Backwards-compatible alias for older callers that expect `_stop_beep`.
    def _stop_beep(self) -> None:
        """Compatibility wrapper for older code that calls _stop_beep."""
        return self.stop_beep()

    def alarm_loop(self, get_distance_func):
        """
        Continuously beep while in alarm range.
        get_distance_func: a function that returns current distance (float or None)
        Handles None readings by treating them as safe distance.
        """
        print(f"Entering alarm loop. Will beep while distance < {DANGER_DISTANCE_CM}cm.")
        print(f"Beep intervals: {INTERVAL_CRITICAL}s (critical), {INTERVAL_WARNING}s (warning), {INTERVAL_DANGER}s (danger)")
        print("Note: None readings are treated as safe distance (no beeping)")
        if not self._audio_available:
            print("NOTE: Audio is disabled. Only beep messages will be printed.")
            
        while True:
            dist = get_distance_func()
            
            # Handle None reading - treat as safe distance (no beeping)
            if dist is None:
                print("Received None reading - treating as safe distance")
                self._closest_dist = None
                self._curr_duration = None
                time.sleep(SAFE_SLEEP_INTERVAL)
                continue
                
            # If we're outside the alarm region, stop.
            if dist >= DANGER_DISTANCE_CM:
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
