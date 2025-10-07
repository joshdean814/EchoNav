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
        # Send 10µs pulse to trigger
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        # Wait for echo start
        while GPIO.input(ECHO) == 0:
            start = time.time()

        # Wait for echo end
        while GPIO.input(ECHO) == 1:
            end = time.time()

        # Calculate distance (speed of sound = 34300 cm/s)
        duration = end - start
        distance = (duration * 34300) / 2

        print(f"Distance: {distance:.1f} cm")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nExiting...")
    GPIO.cleanup()