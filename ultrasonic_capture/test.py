import RPi.GPIO as GPIO
import time

# Pin setup
TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

try:
    while True:
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        # Wait for echo start
        timeout = time.time() + 0.02
        while GPIO.input(ECHO) == 0:
            start = time.time()
            if time.time() > timeout:
                print("Timeout waiting for ECHO to go high")
                break

        # Wait for echo end
        timeout = time.time() + 0.02
        while GPIO.input(ECHO) == 1:
            end = time.time()
            if time.time() > timeout:
                print("Timeout waiting for ECHO to go low")
                break

        # Calculate distance (speed of sound = 34300 cm/s)
        duration = end - start
        distance = (duration * 34300) / 2

        print(f"Distance: {distance:.1f} cm")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nExiting...")
    GPIO.cleanup()