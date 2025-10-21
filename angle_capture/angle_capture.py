"""This module is responsible for capturing the current steering angle from the RC controller

File: angle_capture.py
Author: Prabandh Battu
Last Modified: 21/10/2025

Utilizes readings from an MPU6050 gyroscope sensor to make its determinations.
"""
import time, math
from mpu6050 import mpu6050
from threading import Thread, Lock, Event
from enum import IntEnum

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from common_api.angle import TurnState
from angle_visual import AngleVisual

# Configuration constants for the gyroscope system.
I2C_ADDR         = 0x68     # Port address of the I2C protocol.
BIAS_SAMPLES     = 200      # Samples to average for bias at startup.
SAMPLE_HZ        = 100      # Loop rate during a sensing event.
LPF_ALPHA        = 0.85     # Alpha value to determine smoothness of the filter.

# Tunable paramters to match controller setup.
VEL_NOISE = 1.5
LEAK_PER_SEC = 0.02
MIN_DEG = -30.0     # Maximum degree to the left (counterclockwise).
MAX_DEG = 30        # Maximum degree to the right (clockwise).
CENTER_TOL = 5.0    # Amount of cushion around 0 deg +/-.

class AngleCapture():
    """Captures and interprets angular movement from the MPU6050 gyroscope sensor.

    Continuously reads rotational data from the gyroscope, filters it, and integrates 
    over time to estimate the yaw angle.
    """
    def __init__(self, debug: bool = False) -> None:
        """Initializes the AngleCapture class.

        Arguments:
            debug (bool): True if debug logging is active.
        """
        self._debug = debug
        self._sensor = mpu6050.mpu6050(I2C_ADDR)
        
        # Internal state to track changes in angle.
        self._turn_state: TurnState = TurnState.IDLE
        self._z_change: float = 0.0
        self._filtered: float = 0.0
        self._yaw_deg: float = 0.0
        self._last_reading: time.time = time.time()
        self._z_axis_bias = self._calibrate()
        
        # Thread controls.
        self._detect_flag: Event = Event()
        self._thread: Optional[Thread] = None
        self._lock = Lock()
        
        # Control to display angle.
        self._angle_vis = AngleVisual()
        
    def _calibrate(self) -> float:
        """Calibrates the gyroscope by averaging several readings.
         
        Determines the baseline bias (offset). This reduces drift caused by sensor noise.

        Returns:
            (float): bias calculated from the samples.
        """
        if self._debug:
            print("[DEBUG] Calibrating gyroscope...do not move!")
            
        bias_sum = 0.0
        # Calculate the average variability between readings.
        for _ in range(BIAS_SAMPLES):
            z_angle = self._sensor.get_gyro_data()["z"] # Reports in deg/s.
            bias_sum += z_angle
            time.sleep(1.0 / SAMPLE_HZ)
        z_axis_bias = bias_sum / BIAS_SAMPLES
        
        if self._debug:
            print(f"[DEBUG] Gyroscope z-axis bias: {z_axis_bias} deg/s.")
            
        return z_axis_bias
                    
    def start(self) -> None:
        """Start the detection loop once. Safe to call multiple times."""
        if self._thread and self._thread.is_alive():
            return
            
        # Begin with idle, down arrow display.
        self._angle_vis.display_arrow_from_turn(TurnState.IDLE)
            
        self._detect_flag.set()
        self._thread = Thread(target=self._detect_loop)
        self._thread.start()
        
    def _clamp(self, x: float, lo: float, hi: float) -> float:
        """Restricts a value to remain within a specified range.
        
        Arguments:
            x (float): value to clamp.
            lo (float): bottom of clamp range.
            hi (float): top of clamp range.
            
        Returns:
            (float):  clamped value.
        """
        if x < lo:
            return lo
        if x > hi:
            return hi
        return x
        
    def _direction_from_yaw(self) -> TurnState:
        """Determines the vehicle's turning state based on current yaw angle.

        Returns:
            (TurnState): current steering direction the car is headed in.
        """
        if self._yaw_deg + CENTER_TOL < 0.0:
            return TurnState.LEFT_TURN
        if self._yaw_deg - CENTER_TOL > 0.0:
            return TurnState.RIGHT_TURN
        return TurnState.IDLE
        
    def _detect_loop(self) -> None:
        """Main sensor loop that runs continuously in a background thread.

        Reads gyroscope data, applies low-pass filtering, integrates the
        rotation to estimate yaw, clamps the result within bounds, and updates
        the turn display when the direction changes.
        """
        while self._detect_flag.is_set():
            curr_time = time.time()
            dt = curr_time - self._last_reading
            if dt <= 0: 
                continue
            self._last_reading = curr_time

            # Find current (bias corrected) angle reading.
            self._z_change = self._sensor.get_gyro_data()["z"] - self._z_axis_bias

            # Low-pass filter the rate to reduce any noise in the reading.
            self._filtered = LPF_ALPHA * self._z_change + (1 - LPF_ALPHA) * self._z_change
            
            # integrate to angle (optional; useful for angle-based triggers)
            self._yaw_deg += self._filtered * dt
            
            if abs(self._filtered) < VEL_NOISE:
                self._yaw_deg -= self._yaw_deg * (LEAK_PER_SEC * dt)
            
            self._yaw_deg = self._clamp(self._yaw_deg, MIN_DEG, MAX_DEG)
            
            # Check if steering is in a new direction.
            new_turn_state = self._direction_from_yaw()
            if self._turn_state != new_turn_state:
                self._turn_state = new_turn_state
                if self._debug:
                    print(f"[DEBUG] New turn state: {self._turn_state}")
                    self._angle_vis.display_arrow_from_turn(self._turn_state)
                    
         
            # Wait until next reading.
            time.sleep(max(0, (1.0 / SAMPLE_HZ) - (time.time() - curr_time)))
        
    def stop(self) -> None:
        """Signal the thread to stop and wait for it to exit."""
        if self._debug:
            print("[DEBUG] Stopping detection thread...")
        self._detect_flag.clear()
        if self._thread:
            self._thread.join(timeout=1)
            self._thread = None
            
        self._angle_vis.clear_display()