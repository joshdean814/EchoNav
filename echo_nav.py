from time import sleep
from speaker_beep import SpeakerBeep
from ultrasonic_capture import UltrasonicCapture

class EchoNav():
    def __init__(self):
        self._ultrason_cap = UltrasonicCapture()
        self._speaker_beep = SpeakerBeep()

    def start(self) -> None:
        while True:
            print("PING")
            sleep(1)

def main():
    echo_nav = EchoNav()
    echo_nav.start()


if __name__=="__main__":
    main()