
"""Main controller module for the EchoNav ultrasonic navigation system.

File: echo_nav.py
Author: Josh Dean
Last Modified: 21/10/2025

This module defines the EchoNav class, which integrates ultrasonic distance sensing,
gyroscope angle detection, and speaker-based feedback into a cohesive navigation system.
The EchoNav system continuously reads sensor data and provides real-time feedback
to assist users in detecting obstacles within their surroundings.
"""
from time import sleep
from sense_hat import SenseHat
import threading
from typing import Optional

from speaker_beep import SpeakerBeep
from ultrasonic_capture import UltrasonicCapture
from angle_capture import AngleCapture

class EchoNav():
    """Main controller for the EchoNav system.

    The EchoNav class manages ultrasonic sensor input, angular orientation tracking, 
    and speaker feedback to create an obstacle detection and navigation system.
    It also runs a background control loop to continuously process sensor readings 
    and provide real-time audio feedback.
    """
    def __init__(self) -> None:
        """Initializes the EchoNav controller and its components."""
        self._debug: bool = True
        self._thread: Optional[threading.Thread] = None
        self._running: bool = False
        self._active_flag: threading.Event = threading.Event()
        self._ultrason_cap = UltrasonicCapture(debug=self._debug)
        self._angle_cap = AngleCapture(debug=self._debug)
        self._speaker_beep = SpeakerBeep(debug=self._debug)
        
    def _control_loop(self) -> None:
        """Main processing loop for EchoNav.

        Continuously reads ultrasonic sensor data, updates speaker feedback, 
        and handles timing for real-time obstacle detection.
        """
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
        """Starts or stops the main control loop depending on the current state.
        When stopped, it instructs the user to press the joystick to restart.
        """
        if self._running:
            self._stop()
            print("Press the joystick to restart the sensors...")
        else:
            self._start()

    def _start(self) -> None:
        """
        Starts the EchoNav control loop and all active components.

        Initializes sensor and speaker modules, sets the active flag, 
        and spawns the control loop thread.
        """
        if self._running:
            return
        self._speaker_beep.start()
        self._angle_cap.start()
        self._active_flag.set()
        
        # Start a thread for the control loop.
        self._thread = threading.Thread(target=self._control_loop)
        self._thread.start()
        self._running = True

    def _stop(self) -> None:
        """
        Stops the EchoNav system safely.

        Stops all sensor and feedback components, and joins the main loop thread.
        """
        if not self._running:
            return
        self._active_flag.clear()
        self._speaker_beep.stop()
        self._angle_cap.stop()
        
        # Wait for the control thread to join.
        if self._thread: 
            self._thread.join(timeout=1)
            self._thread = None
            
        self._running = False

    def shutdown(self) -> None:
        """Performs a complete system shutdown.

        Stops all running components and releases ultrasonic sensor resources.
        """
        if self._debug:
            print("Shutting down EchoNav...")
        self._stop()
        self._ultrason_cap.shutdown()

def main() -> None:
    """
    Main entry point to the program.

    Toggles execution based on pressing the joystick in the RaspPi SenseHat.
    Exits gracefully with `Ctrl-C`.
    """ 
    echo_nav = EchoNav()
    sense = SenseHat()
    
    print("Press the joystick to toggle the program!")
    try:
        while True:
            # Capture middle presses of the joystick and alert program.
            for event in sense.stick.get_events():
                if event.action == "pressed" and event.direction == "middle":
                    echo_nav.toggle_program()
    except KeyboardInterrupt:
        # Catch ctrl-c and exit.
        echo_nav.shutdown()
        exit(0)

if __name__=="__main__":
    main()