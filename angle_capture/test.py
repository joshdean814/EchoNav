import smbus, time, struct

bus = smbus.SMBus(1)
addr = 0x68

# wake device
bus.write_byte_data(addr, 0x6B, 0)
time.sleep(0.1)

def read_word(reg):
    hi, lo = bus.read_i2c_block_data(addr, reg, 2)
    val = (hi << 8) | lo
    return val - 65536 if val & 0x8000 else val

while True:
    gx = read_word(0x43)
    gy = read_word(0x45)
    gz = read_word(0x47)
    print("Gyro:", gx, gy, gz)
    time.sleep(0.5)
