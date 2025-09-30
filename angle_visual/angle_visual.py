from ..common_api.angle import *
from typing import List
import numpy as np

# Validates an angle reading and passes to 
def check_angle(reading: AngleReading) -> None:
    if not reading.valid:
        return
    
    raise NotImplementedError()


