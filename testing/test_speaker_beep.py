import sys
import os
import time
import numpy as np
import sounddevice as sd

sys.path.append(os.path.dirname(__file__))

from speaker_beep import SpeakerBeep
from common_api.distance import DistanceReading, CarCorner

def test_closest_dist(speaker_beep, short_distances):
    speaker_beep.update_closest(short_distances)
    assert speaker_beep._closest_dist == 5