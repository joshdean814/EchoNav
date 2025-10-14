from time import sleep
from speaker_beep import SpeakerBeep
from ultrasonic_capture import UltrasonicCapture

class EchoNav():
    def __init__(self):
        self._debug = True
        self._ultrason_cap = UltrasonicCapture(debug=self._debug)
        self._speaker_beep = SpeakerBeep()

    def start(self) -> None:
        if self._debug:
            print("Starting up EchoNav...")
        try:
            while True:
                readings = self._ultrason_cap.read_all()
                if self._debug:
                    print(f"[DEBUG] Readings: {readings}")
                self._speaker_beep.update_closest(readings)
                sleep(5)
                
        except KeyboardInterrupt:
            if self._debug:
                print("Shutting down EchoNav...")
            self._ultrason_cap.shutdown()
            self._speaker_beep.stop_beep()
            exit(0)       

def main():
    echo_nav = EchoNav()
    echo_nav.start()


if __name__=="__main__":
    main()
