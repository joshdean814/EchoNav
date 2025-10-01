from typing import Optional, List

from ..common_api.distance import CarCorner, DistanceReading

class UltrasonicCapture():
    def __init__(self, trig_pin: int, echo_pin: int):
        pass
        # TODO: initialize the 4 sensors, if needed.

    def read_all(self) -> List[DistanceReading]:
        pass

    def _read_distance(self) -> DistanceReading:
        pass