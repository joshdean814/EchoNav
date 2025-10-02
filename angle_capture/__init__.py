import time
import glowbit

# --- Setup GlowBit Matrix (8x8) ---
matrix = glowbit.matrix8x8()
matrix.pixelsFill((0, 0, 0))
matrix.pixelsShow()


# --- Helper: clear screen ---
def clear():
    matrix.pixelsFill((0, 0, 0))
    matrix.pixelsShow()


# --- Helper: Convert (row, col) -> GlowBit index ---
def rc_to_index(row, col):
    return row * 8 + col  # 8 columns per row


# --- Draw arrow ---
def draw_arrow(direction="straight", color=(255, 0, 0)):
    clear()
    arrow_pixels = []

    if direction == "straight":  # UP arrow
        # vertical shaft
        for r in range(3, 8):
            arrow_pixels.append(rc_to_index(r, 3))
            arrow_pixels.append(rc_to_index(r, 4))
        # tip
        arrow_pixels += [
            rc_to_index(2, 2), rc_to_index(2, 5),
            rc_to_index(1, 1), rc_to_index(1, 6),
            rc_to_index(0, 0), rc_to_index(0, 7)
        ]

    elif direction == "left":
        for c in range(2, 7):
            arrow_pixels.append(rc_to_index(4, c))
            arrow_pixels.append(rc_to_index(3, c))
        arrow_pixels += [
            rc_to_index(2, 2), rc_to_index(5, 2),
            rc_to_index(1, 1), rc_to_index(6, 1),
            rc_to_index(0, 0), rc_to_index(7, 0)
        ]

    elif direction == "right":
        for c in range(1, 6):
            arrow_pixels.append(rc_to_index(4, c))
            arrow_pixels.append(rc_to_index(3, c))
        arrow_pixels += [
            rc_to_index(2, 5), rc_to_index(5, 5),
            rc_to_index(1, 6), rc_to_index(6, 6),
            rc_to_index(0, 7), rc_to_index(7, 7)
        ]

    # Light up pixels
    for i in arrow_pixels:
        matrix.pixelSet(i, color)

    matrix.pixelsShow()


# --- Decide arrow based on tyre angle ---
def angle_to_arrow(theta):
    if -15 <= theta <= 15:
        return "straight"
    elif theta < -15:
        return "left"
    elif theta > 15:
        return "right"


# --- Main loop (simulate tyre angles) ---
test_angles = [0, -30, 30, -10, 12, 60]

for angle in test_angles:
    direction = angle_to_arrow(angle)
    print(f"Tyre angle: {angle}° -> {direction}")
    draw_arrow(direction, (0, 255, 0))
    time.sleep(1)
