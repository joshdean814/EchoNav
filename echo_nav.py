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
            sleep(0.00001)
        if self._debug:
            print("EchoNav loop exited")
            
    def toggle_program(self) -> None:
        self._running = not self._running
        if self._running:
            self._start()
        else:
            self._stop()
            print("Press the joystick to restart the sensors...")

    def _start(self):
        self._active_flag.set()
        self._thread = threading.Thread(target=self._control_loop)
        self._thread.start()

    def _stop(self):
        self._active_flag.clear()
        self._speaker_beep.stop_beep()
        
        if self._thread: 
            self._thread.join()
            self._thread = None

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
                    echo_nav.toggle_program()
    except KeyboardInterrupt:
        echo_nav.shutdown()
        exit(0)

if __name__=="__main__":
    main()
