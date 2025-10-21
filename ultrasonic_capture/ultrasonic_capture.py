"""This module provides ultrasonic distance sensing for the EchoNav system.

File: ultrasonic_capture.py
Author: Josh Dean
Last Modified: 21/10/2025

This module defines two main classes:

- UltrasonicSensor: handles a single ultrasonic sensor, managing GPIO setup,
  triggering, timing, and distance measurement.
- UltrasonicCapture: manages multiple sensors (front, rear, etc.), aggregates
  their readings, and handles cleanup.

The system operates on the principle that the time taken for a sound pulse to
travel to an obstacle and back can be used to calculate distance. It uses
the Raspberry Pi's GPIO pins for trigger and echo control.
"""
import RPi.GPIO as GPIO
import time
import statistics
from typing import Optional, List, Tuple

from common_api.distance import CarCorner, DistanceReading

# We know the speed of sound is 373 m/s, so 37300 cm/s
# Signal must go and come back, so divide by 2: 37300 / 2 = 17150
SOUND_SPEED = 17150
PULSE_DUR = 0.0001  # 10 microsecond pulse.
TIMEOUT_DUR = 3     # 3 second timeout.
NUM_TRIALS = 3      # Times to try reading.
MAX_DEV = 3.0       # Max deviation between readings (in cm).

# Use the GPIO pin names, not physical pin locations.
GPIO.setmode(GPIO.BCM)

class UltrasonicSensor():
    """
    Represents a single ultrasonic sensor module connected to a specific 
    position (corner) on the vehicle or device.

    Handles GPIO initialization, trigger pulse emission, echo timing, and
    conversion to distance readings. Includes a brief dry-run on initialization
    to verify hardware function.
    """
    def __init__(self, corner: CarCorner, debug: bool = False) -> None:
        """Initializes an ultrasonic sensor.

        Arguments:
            corner (CarCorner): Which physical corner we are attached to.
            debug (bool): True if we logging debugging statements.
        """
        self._corner = corner
        self._trig_pin, self._echo_pin = self._corner.pins
        
        if debug:
            print(f"[DEBUG] Setting up sensor: {self._corner.print_name}")
            print(f"[DEBUG] TRIG: {self._trig_pin}, ECHO: {self._echo_pin}")
        
        # Attempt to communicate with the sensor.
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
            
        try:
            test_distance = self._read_one_distance()
        except Exception as e:
            print(f"Critical error while testing sensor: {self._corner.print_name}!")
            print(f"Error: {e}")
            exit(-1)
        
        if debug:
            print(f"[DEBUG] Test reading result: {test_distance}")
            print(f"[DEBUG] Sensor: {self._corner.print_name} setup!")
        
    def _read_one_distance(self) -> Optional[float]:
        """Emits one ultrasonic pulse and measures the round-trip time to compute distance.

        Returns:
            (float | None): a single distance measurement in centimeters, or None if timed out.
        """
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
                if self._debug:
                    print(f"Sensor: {self._corner.print_name} timed out during reading!")
                return None
            
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
        """Determines whether a group of distance readings is consistent.

        Arguments:
            readings (List[float]): list of three successive readings from the same sensor.

        Returns:
            (bool, float | None): The first value indicates if the readings are acceptable, 
            the second is the computed mean, or None if it was invalid.
        """

        # Ensure all values are present, and positive, non-null.
        cleaned = [r for r in readings if r is not None and r >= 0]
        if len(cleaned) < 2:
            return False, None
        
        mean = statistics.mean(cleaned)
        deviations = [
            abs(r - mean)
            for r in cleaned
        ]
        # Check if deviation is acceptable
        return max(deviations) <= MAX_DEV, mean
    
    def read_distance(self) -> DistanceReading:
        """Performs multiple readings to ensure accuracy.

        Returns: 
            (DistanceReading): reading DTO with a valid or None distance value.
        """
        distances: List[float] = [
            self._read_one_distance()
            for _ in range(NUM_TRIALS)
        ]

        stable, mean = self._is_stable(distances)
        dr = DistanceReading(self._corner, mean)
        if not stable:
            dr.distance = None

        return dr
        
    @property
    def name(self) -> str:
        """Returns the sensor’s descriptive name."""
        return self._corner.print_name

class UltrasonicCapture():
    """Manages multiple ultrasonic sensors and coordinates distance readings.

    This class initializes all available ultrasonic sensors defined in the
    CarCorner enum and provides a unified interface to read distance
    data from each one. It handles setup, collection, and cleanup of GPIO
    resources used by the sensors.
    """

    def __init__(self, debug: bool = True):
        """Initializes the capturing controller.
        
        Arguments:
            debug (bool): True if debug logging is active.
        """
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
        """Reads distance data from all ultrasonic sensors.

        Iterates through each sensor, collecting distance readings.
        If a sensor fails to provide a reading, the error is logged but
        execution continues for the remaining sensors.

        Returns:
            (List[DistanceReading]): list of reading DTO containing distance data for each sensor position.
        """
        readings: List[DistanceReading] = []
        
        # Attempt to read all of the sensors.
        for sensor in self._sensors:
            try:
                reading = sensor.read_distance()
            except Exception as e:
                print(f"Error while reading sensor: {sensor.name}!")
                print(f"Error: {e}")
                
            readings.append(reading)
            
        return readings

    def shutdown(self) -> None:
        """Safely shuts down all ultrasonic sensors."""
        GPIO.cleanup()