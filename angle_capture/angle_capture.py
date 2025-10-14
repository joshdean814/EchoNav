import time, math
import smbus

# I2C setup
BUS_NUM = 1
ADDR    = 0x68      # use 0x69 if AD0=HIGH

# Registers
WHO_AM_I   = 0x75
PWR_MGMT_1 = 0x6B
ACCEL_CFG  = 0x1C
GYRO_CFG   = 0x1B
ACCEL_XOUT_H = 0x3B

# Sensitivities for ±2g and ±250 dps
ACCEL_SENS = 16384.0
GYRO_SENS  = 131.0

bus = smbus.SMBus(BUS_NUM)

def r8(reg):
    return bus.read_byte_data(ADDR, reg)

def w8(reg, val):
    bus.write_byte_data(ADDR, reg, val & 0xFF)

def read_block(reg, length):
    return bus.read_i2c_block_data(ADDR, reg, length)

def to_int16(hi, lo):
    val = (hi << 8) | lo
    return val - 65536 if val & 0x8000 else val

# ---- bring-up ----
# Check presence
who = r8(WHO_AM_I)
print(f"WHO_AM_I = 0x{who:02X}")
if who != 0x68:
    raise RuntimeError("MPU6050 not responding (check address/wiring)")

# Wake device
w8(PWR_MGMT_1, 0x00)
time.sleep(0.05)

# Force known ranges: accel ±2g, gyro ±250 dps
w8(ACCEL_CFG, 0x00)
w8(GYRO_CFG,  0x00)

print("Reading... Press Ctrl+C to stop.")
time.sleep(0.05)

prev = time.time()
roll, pitch = 0.0, 0.0
alpha = 0.98

while True:
    # Read 14 bytes starting at ACCEL_XOUT_H
    # ax,ay,az,temp,gx,gy,gz (each int16)
    b = read_block(ACCEL_XOUT_H, 14)

    ax = to_int16(b[0], b[1]) / ACCEL_SENS
    ay = to_int16(b[2], b[3]) / ACCEL_SENS
    az = to_int16(b[4], b[5]) / ACCEL_SENS

    gx = to_int16(b[8],  b[9])  / GYRO_SENS
    gy = to_int16(b[10], b[11]) / GYRO_SENS
    # gz = to_int16(b[12], b[13]) / GYRO_SENS  # not used for roll/pitch

    now = time.time()
    dt = now - prev
    prev = now

    # Accelerometer angles (degrees) — NOTE the squares are **Ax**2 and **Az**2 etc.
    acc_roll  = math.degrees(math.atan2(ay, math.sqrt(ax*ax + az*az)))
    acc_pitch = math.degrees(math.atan2(-ax, math.sqrt(ay*ay + az*az)))

    # Integrate gyro
    roll  = alpha * (roll  + gx * dt) + (1 - alpha) * acc_roll
    pitch = alpha * (pitch + gy * dt) + (1 - alpha) * acc_pitch

    print(f"Roll: {roll:6.2f}°  Pitch: {pitch:6.2f}°")
    time.sleep(0.05)
