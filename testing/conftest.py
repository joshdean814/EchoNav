import pytest

from typing import List
from speaker_beep import SpeakerBeep
from common_api.distance import DistanceReading, CarCorner

@pytest.fixture
def speaker_beep() -> SpeakerBeep:
    """Creates a speaker beep for testing."""
    speaker_beep = SpeakerBeep()
    return speaker_beep

@pytest.fixture
def short_distances() -> List[DistanceReading]:
    distances = [
        DistanceReading(CarCorner.BACK_LEFT, 5),
        DistanceReading(CarCorner.BACK_LEFT, 10),
        DistanceReading(CarCorner.BACK_LEFT, 15),
        DistanceReading(CarCorner.BACK_LEFT, 20)
    ]
    return distances