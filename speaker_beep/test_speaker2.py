from speaker_beep import SpeakerBeep
from common_api.distance import DistanceReading, CarCorner
import time

'''
[DEBUG] Readings: 
    [
        DistanceReading(corner=<CarCorner.BACK_LEFT: 0>, distance=206.69666666666666), 
        DistanceReading(corner=<CarCorner.BACK_RIGHT: 1>, distance=21.366666666666667)
    ]
'''
speaker_beep = SpeakerBeep()

distances = [
    DistanceReading(CarCorner.BACK_LEFT, 206.696),
    DistanceReading(CarCorner.BACK_RIGHT, 21.366)
]

speaker_beep.update_closest(distances)

time.sleep(10)