"""This module creates an interface for the UltrasonicCapture and SpeakerBeep modules.

File: distance.py
Author: Josh Dean
Last Modified: 21/10/2025
"""
from enum import IntEnum
from typing import Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

class CarCorner(IntEnum):
    """Defines the physical placement of ultrasonic sensors on the vehicle."""
    BACK_LEFT = 0
    BACK_RIGHT = 1
    FRONT_RIGHT = 2
    FRONT_LEFT = 3
    
    @property
    def print_name(self) -> str:
        """Returns a formatted, human-readable version of the corner name."""
        return self.name.replace("_", " ").lower().title()
    
    @property
    def pins(self) -> Tuple[int]:
        """
        Returns the GPIO trigger and echo pins associated with this sensor.

        The tuple format is (TRIG_PIN, ECHO_PIN).
        """
        pin_map = {
            self.BACK_RIGHT : (17, 27),
            self.BACK_LEFT : (16, 26),
            self.FRONT_RIGHT : (5, 6), 
            self.FRONT_LEFT : (20, 21)
        }
        return pin_map.get(self)
    
@dataclass
class DistanceReading:
    """DTO representing a single distance measurement from one sensor."""
    corner: CarCorner
    distance: Optional[float]