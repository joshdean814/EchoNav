import RPi.GPIO as GPIO
import time

from typing import Optional, List

from common_api.distance import CarCorner, DistanceReading

PULSE_DUR = 0.0001 # 10 microsecond pulse.

""" 
    We know the speed of sound is 373 m/s, so 37300 cm/s
    Signal must go and come back, so divide by 2:
    37300 / 2 = 17150
"""
SOUND_SPEED = 17150
TIMEOUT_DUR = 3 # 3 second timeout.

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
            
        reading = self.read_distance()
        
        if debug:
            print(f"[DEBUG] Test reading result: {reading.distance}")
            print(f"[DEBUG] Sensor: {self._corner.print_name} setup!")
        
    def read_distance(self) -> DistanceReading:
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
        
        return DistanceReading(
            corner=self._corner,
            distance=distance
        )
        

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
        pass
