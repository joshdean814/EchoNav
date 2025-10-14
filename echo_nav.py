from time import sleep
from sense_hat import SenseHat
import threading
from typing import Optional

from speaker_beep import SpeakerBeep
from ultrasonic_capture import UltrasonicCapture

class EchoNav():
    def __init__(self):
        self._debug: bool = True
        self.active: bool = False
        self._thread: Optional[threading.Thread] = None
        self._ultrason_cap = UltrasonicCapture(debug=self._debug)
        self._speaker_beep = SpeakerBeep()

    def _control_loop(self):
        if self._debug:
            print("Starting up EchoNav loop...")
        while self.active:
            readings = self._ultrason_cap.read_all()
            if self._debug:
                print(f"[DEBUG] Readings: {readings}")
            self._speaker_beep.update_closest(readings)
        if self._debug:
            print("EchoNav loop exited")

    def start(self):
        if self.active:
            return  # already running
        self.active = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        if not self.active:
            return
        self.active = False
        self._speaker_beep.stop_beep()

    def shutdown(self) -> None:
        if self._debug:
            print("Shutting down EchoNav...")
        self.stop()
        self._ultrason_cap.shutdown()
                
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
