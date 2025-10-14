from time import sleep
from sense_hat import SenseHat
import threading
from typing import Optional

from speaker_beep import SpeakerBeep
from ultrasonic_capture import UltrasonicCapture

class EchoNav():
    def __init__(self):
        self._debug: bool = True
        self._thread: Optional[threading.Thread] = None
        self._running: bool = False
        self._active_flag: threading.Event = threading.Event()
        self._ultrason_cap = UltrasonicCapture(debug=self._debug)
        self._speaker_beep = SpeakerBeep(debug=self._debug)

    def _control_loop(self):
        if self._debug:
            print("Starting up EchoNav loop...")
        while self._active_flag.is_set():
            readings = self._ultrason_cap.read_all()
            if self._debug:
                print(f"[DEBUG] Readings: {readings}")
            self._speaker_beep.update_closest(readings)
            sleep(0.05)
        if self._debug:
            print("EchoNav loop exited")
            
    def toggle_program(self) -> None:
        if self._running:
            self._stop()
            print("Press the joystick to restart the sensors...")
        else:
            self._start()

    def _start(self):
        if self._running:
            return
        self._speaker_beep.start()
        self._active_flag.set()
        self._thread = threading.Thread(target=self._control_loop)
        self._thread.start()
        self._running = True

    def _stop(self):
        if not self._running:
            return
        self._active_flag.clear()
        self._speaker_beep.stop()
        
        if self._thread: 
            self._thread.join(timeout=1)
            self._thread = None
            
        self._running = False

    def shutdown(self) -> None:
        if self._debug:
            print("Shutting down EchoNav...")
        self._stop()
        self._ultrason_cap.shutdown()
                
def main():
    echo_nav = EchoNav()
    sense = SenseHat()
    
    print("Press the joystick to toggle the program!")
    try:
        while True:
            for event in sense.stick.get_events():
                if event.action == "pressed" and event.direction == "middle":
                    print("here")
                    echo_nav.toggle_program()
    except KeyboardInterrupt:
        echo_nav.shutdown()
        exit(0)

if __name__=="__main__":
    main()
