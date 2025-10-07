import RPi.GPIO as GPIO
import time

# Pin setup – matches your wiring
TRIG = 27      # white wire on physical pin 13
ECHO = 17      # yellow wire on physical pin 11

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

try:
    while True:
        # Send a short trigger pulse
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        # Wait for echo to go HIGH
        timeout = time.time() + 0.02
        while GPIO.input(ECHO) == 0:
            start = time.time()
            if time.time() > timeout:
                print("Timeout waiting for ECHO to go high")
                start = None
                break

        # Wait for echo to go LOW
        timeout = time.time() + 0.02
        while start and GPIO.input(ECHO) == 1:
            end = time.time()
            if time.time() > timeout:
                print("Timeout waiting for ECHO to go low")
                end = None
                break

        # Calculate and print distance if valid
        if start and end:
            duration = end - start
            distance = (duration * 34300) / 2   # cm
            print(f"Distance: {distance:.1f} cm")
        else:
            print("No valid echo")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    GPIO.cleanup()
