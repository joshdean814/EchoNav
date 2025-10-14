from speaker_beep.speaker_beep import SpeakerBeep
from types import SimpleNamespace as S

b = SpeakerBeep()
for d in [5,15,25,40,60]:
    b.update_closest([S(distance=d)], play=False)
    if b._curr_duration is None:
        print(f"{d} -> None")
    else:
        print(f"{d} -> {b._curr_duration:.6f}")
