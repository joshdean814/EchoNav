from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class AngleReading:
    angle: float
    timestamp: datetime = field(default_factory=lambda: datetime.now())
    valid: bool = field(default=True)