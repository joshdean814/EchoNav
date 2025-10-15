import time, math
from mpu6050 import mpu6050   # if your lib exposes MPU6050 class instead, change import accordingly

I2C_ADDR = 0x68               # or 0x6A/0x69 per your hardware
sensor = mpu6050(I2C_ADDR)

# --- params to tune ---
SAMPLE_HZ        = 100        # loop rate
VEL_THRESH       = 8.0        # deg/s: must exceed this to count as a turn
VEL_RELEASE      = 4.0        # deg/s: drop below this to end the turn (hysteresis)
LPF_ALPHA        = 0.85       # 0..1, higher = smoother
ANGLE_TRIP       = 10.0       # deg: optional, declare a turn event after this much yaw
BIAS_SAMPLES     = 200        # samples to average for bias at startup
# ----------------------

# 1) calibrate gyro Z bias (hold device still!)
print("Calibrating gyro bias...")
bias_sum = 0.0
for _ in range(BIAS_SAMPLES):
    gz = sensor.get_gyro_data()['z']   # deg/s (this lib reports in deg/s)
    bias_sum += gz
    time.sleep(1.0 / SAMPLE_HZ)
bias_z = bias_sum / BIAS_SAMPLES
print(f"Bias Z = {bias_z:.3f} deg/s")

# state
gz_lpf = 0.0
yaw_deg = 0.0
state = "idle"   # idle | turning_left | turning_right
last_t = time.time()

def update_state(gz_f):
    global state
    if state == "idle":
        if gz_f > VEL_THRESH:
            state = "turning_right"; print("TURN RIGHT start")
        elif gz_f < -VEL_THRESH:
            state = "turning_left";  print("TURN LEFT start")
    elif state == "turning_right":
        if gz_f < VEL_RELEASE:
            state = "idle";          print("TURN RIGHT end")
    elif state == "turning_left":
        if gz_f > -VEL_RELEASE:
            state = "idle";          print("TURN LEFT end")

while True:
    t = time.time()
    dt = t - last_t
    if dt <= 0: 
        continue
    last_t = t

    gz = sensor.get_gyro_data()['z'] - bias_z  # bias-corrected deg/s

    # low-pass filter the rate
    gz_lpf = LPF_ALPHA * gz_lpf + (1 - LPF_ALPHA) * gz

    # integrate to angle (optional; useful for angle-based triggers)
    yaw_deg += gz_lpf * dt

    # velocity-based left/right detection with hysteresis
    update_state(gz_lpf)

    # optional: angle-based event (e.g., short nudge)
    if abs(yaw_deg) >= ANGLE_TRIP:
        if yaw_deg > 0:
            print(f"ANGLE TRIP: RIGHT {yaw_deg:.1f}°")
        else:
            print(f"ANGLE TRIP: LEFT  {yaw_deg:.1f}°")
        yaw_deg = 0.0  # reset accumulator after event

    time.sleep(max(0, (1.0 / SAMPLE_HZ) - (time.time() - t)))
