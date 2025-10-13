import smbus
import time
import math

# MPU6050 Registers and Address
MPU6050_ADDR = 0x68
PWR_MGMT_1   = 0x6B
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

# Initialize I2C bus
bus = smbus.SMBus(1)
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

def read_raw_data(addr):
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr + 1)
    value = ((high << 8) | low)
    if value > 32768:
        value -= 65536
    return value

# Sensitivity scale factors
ACCEL_SENSITIVITY = 16384.0  # LSB/g for ±2g
GYRO_SENSITIVITY  = 131.0    # LSB/(°/s) for ±250°/s

# Complementary filter coefficient
alpha = 0.98

# Initialize angles
angle_x = 0.0
angle_y = 0.0

prev_time = time.time()

print("Measuring stable angles with complementary filter...")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        # Read accelerometer data
        acc_x = read_raw_data(ACCEL_XOUT_H)
        acc_y = read_raw_data(ACCEL_YOUT_H)
        acc_z = read_raw_data(ACCEL_ZOUT_H)

        # Read gyroscope data
        gyro_x = read_raw_data(GYRO_XOUT_H)
        gyro_y = read_raw_data(GYRO_YOUT_H)
        gyro_z = read_raw_data(GYRO_ZOUT_H)

        # Convert to physical units
        Ax = acc_x / ACCEL_SENSITIVITY
        Ay = acc_y / ACCEL_SENSITIVITY
        Az = acc_z / ACCEL_SENSITIVITY

        Gx = gyro_x / GYRO_SENSITIVITY
        Gy = gyro_y / GYRO_SENSITIVITY
        Gz = gyro_z / GYRO_SENSITIVITY

        # Calculate time difference
        curr_time = time.time()
        dt = curr_time - prev_time
        prev_time = curr_time

        # Calculate accelerometer angles (degrees)
        acc_angle_x = math.degrees(math.atan2(Ay, math.sqrt(Ax*2 + Az*2)))
        acc_angle_y = math.degrees(math.atan2(-Ax, math.sqrt(Ay*2 + Az*2)))

        # Integrate gyro rates to get angles
        gyro_angle_x = angle_x + Gx * dt
        gyro_angle_y = angle_y + Gy * dt

        # Apply complementary filter
        angle_x = alpha * gyro_angle_x + (1 - alpha) * acc_angle_x
        angle_y = alpha * gyro_angle_y + (1 - alpha) * acc_angle_y

        print(f"Roll (X): {angle_x:6.2f}°,  Pitch (Y): {angle_y:6.2f}°")

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nStopped.")