import RPi.GPIO as GPIO
import time
import statistics

from typing import Optional, List, Tuple

from common_api.distance import CarCorner, DistanceReading

""" 
    We know the speed of sound is 373 m/s, so 37300 cm/s
    Signal must go and come back, so divide by 2:
    37300 / 2 = 17150
"""
SOUND_SPEED = 17150
PULSE_DUR = 0.0001  # 10 microsecond pulse.
TIMEOUT_DUR = 3     # 3 second timeout.
NUM_TRIALS = 3      # Times to try reading.
MAX_DEV = 3.0       # Max deviation between readings (in cm).

# Use the GPIO pin names, not physical pin locations.
GPIO.setmode(GPIO.BCM)

class UltrasonicSensor():
    def __init__(self, corner: CarCorner, debug: bool = False):
        self._corner = corner
        self._trig_pin, self._echo_pin = self._corner.pins
        
        if debug:
            print(f"[DEBUG] Setting up sensor: {self._corner.print_name}")
            print(f"[DEBUG] TRIG: {self._trig_pin}, ECHO: {self._echo_pin}")
        
        try:
            GPIO.setup(self._trig_pin, GPIO.OUT)
            GPIO.setup(self._echo_pin, GPIO.IN)
        except Exception as e:
            print(f"Failed to set-up sensor: {self._corner.print_name}")
            print(f"Error: {e}")
            exit(-1)
        
        if debug:
            print("[DEBUG] Allowing sensor to settle...")
        time.sleep(2)
        
        
        if debug:
            print("[DEBUG] Attempting a dry-fire")
            
        distance = self._read_one_distance()
        
        if debug:
            print(f"[DEBUG] Test reading result: {distance}")
            print(f"[DEBUG] Sensor: {self._corner.print_name} setup!")
        
    def _read_one_distance(self) -> float:
        # Sleep 50 ms to prevent cross-talk collisions.
        time.sleep(0.05)
        
        # Send the trigger signal out for 10 ms.
        GPIO.output(self._trig_pin, True)
        time.sleep(PULSE_DUR)
        GPIO.output(self._trig_pin, False)
        
        timeout = time.time() + TIMEOUT_DUR

        # Measure how long it takes to reflect the signal.
        while GPIO.input(self._echo_pin) == 0:
            pulse_start = time.time()
            
            if pulse_start >= timeout:
                raise RuntimeError(f"Sensor: {self._corner.print_name} timed out during reading!")
            
        timeout = time.time() + TIMEOUT_DUR
            
        while GPIO.input(self._echo_pin) == 1:
            pulse_end = time.time()
            
            if pulse_end >= timeout:
                raise RuntimeError(f"Sensor: {self._corner.print_name} timed out during reading!")
            
        # Calculate the final distance measurement.
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * SOUND_SPEED
        distance = round(distance, 2)
        
        return distance
    
    def _is_stable(self, readings: List[float]) -> Tuple[bool, Optional[float]]:
        
        # Ensure all values are present, and positive, non-null.
        cleaned = [r for r in readings if r is not None and r >= 0]
        if len(cleaned) < 2:
            return False, None
        
        mean = statistics.mean(cleaned)
        deviations = [
            abs(r - mean)
            for r in cleaned
        ]
        return max(deviations) <= MAX_DEV, mean
    
    def read_distance(self) -> DistanceReading:
        distances: List[float] = [
            self._read_one_distance()
            for _ in range(NUM_TRIALS)
        ]
        
        print(distances)

        stable, mean = self._is_stable(distances)
        dr = DistanceReading(self._corner, mean)
        if not stable:
            dr.distance = None

        return dr

class UltrasonicCapture():
    def __init__(self, debug: bool = True):
        GPIO.setmode(GPIO.BCM)
        
        if debug:
            print("[DEBUG] Initializing up all sensors")
            
        self._sensors: List[UltrasonicSensor] = [
            UltrasonicSensor(corner, debug=debug)
            for corner in CarCorner
        ]
        
        if debug:
            print("[DEBUG] System setup, ready for readings!")

    def read_all(self) -> List[DistanceReading]:
        return [
            self._sensors[corner.value].read_distance()
            for corner in CarCorner
        ]

    def shutdown(self) -> None:
        GPIO.cleanup()
