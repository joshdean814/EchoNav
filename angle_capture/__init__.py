import time
import glowbit

# --- Setup GlowBit 8x8 Matrix ---
matrix = glowbit.matrix8x8()
matrix.pixelsFill((0, 0, 0))
matrix.pixelsShow()


# --- Helper: clear screen ---
def clear():
    matrix.pixelsFill((0, 0, 0))
    matrix.pixelsShow()


# --- Convert (row, col) -> LED index (0-63) ---
def rc_to_index(row, col):
    return row * 8 + col


# --- Arrow patterns (rows, cols for 8x8) ---
def arrow_pattern(direction):
    if direction == "straight":   # UP arrow
        return [
            (7,3),(7,4),
            (6,3),(6,4),
            (5,3),(5,4),
            (4,3),(4,4),
            (3,2),(3,5),
            (2,1),(2,6),
            (1,0),(1,7)
        ]
    elif direction == "left":
        return [
            (3,6),(4,6),(3,5),(4,5),(3,4),(4,4),  # shaft
            (3,3),(4,3),
            (2,2),(5,2),
            (1,1),(6,1),
            (0,0),(7,0)   # tip
        ]
    elif direction == "right":
        return [
            (3,1),(4,1),(3,2),(4,2),(3,3),(4,3),  # shaft
            (3,4),(4,4),
            (2,5),(5,5),
            (1,6),(6,6),
            (0,7),(7,7)   # tip
        ]
    else:
        return []


# --- Draw arrow on 8x8 matrix ---
def draw_arrow(direction="straight", color=(0, 255, 0)):
    clear()
    for (r, c) in arrow_pattern(direction):
        idx = rc_to_index(r, c)
        matrix.pixelSet(idx, color)
    matrix.pixelsShow()


# --- Map tyre angle (-10°..10°) to arrow ---
def angle_to_arrow(theta):
    if -2 <= theta <= 2:
        return "straight"
    elif theta < -2:
        return "left"
    elif theta > 2:
        return "right"


# --- Demo loop (simulate tyre angles) ---
test_angles = [-10, -5, 0, 5, 10]

for angle in test_angles:
    direction = angle_to_arrow(angle)
    print(f"Tyre angle: {angle}° -> {direction}")
    draw_arrow(direction, (0, 255, 0))
    time.sleep(2)
