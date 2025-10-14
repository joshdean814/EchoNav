from time import sleep
from sense_hat import SenseHat

from speaker_beep import SpeakerBeep
from ultrasonic_capture import UltrasonicCapture

class EchoNav():
    def __init__(self):
        self._debug = True
        self.active = False
        self._ultrason_cap = UltrasonicCapture(debug=self._debug)
        self._speaker_beep = SpeakerBeep()

    def start(self) -> None:
        if self._debug:
            print("Starting up EchoNav...")

        while self.active:
            readings = self._ultrason_cap.read_all()
            if self._debug:
                print(f"[DEBUG] Readings: {readings}")
            self._speaker_beep.update_closest(readings)

    def stop(self) -> None:
        if self._debug:
            print("Stopping EchoNav...")
        self._speaker_beep.stop_beep()

    def shutdown(self) -> None:
        if self._debug:
            print("Shutting down EchoNav...")
        self._ultrason_cap.shutdown()
        self._speaker_beep.stop_beep()
                
def main():
    echo_nav = EchoNav()
    sense = SenseHat()
    
    print("Press the joystick to toggle the program!")
    try:
        while True:
            for event in sense.stick.get_events():
                if event.action == "pressed" and event.direction == "middle":
                    echo_nav.active = not echo_nav.active
                    print(f"Sensing is currently turned: {'on' if echo_nav.active else 'off'}")
                    if echo_nav.active:
                        echo_nav.start()
                    else:
                        echo_nav.stop()
    except KeyboardInterrupt:
        echo_nav.shutdown()
        exit(0)

if __name__=="__main__":
    main()
