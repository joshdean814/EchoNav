from sense_hat import SenseHat
sense = SenseHat()

red = (255, 0, 0)
black = (0, 0, 0)

# Define a down arrow (8x8)
DOWN arrow = [
    black, black, black, red,   red,   black, black, black,
    black, black, black, red,   red,   black, black, black,
    black, black, black, red,   red,   black, black, black,
    black, black, black, red,   red,   black, black, black,
    red,   black, black, red,   red,   black, black, red,
    black, red,   black, red,   red,   black, red,   black,
    black, black, red,   red,   red,   red,   black, black,
    black, black, black, red,   red,   black, black, black
]
# Define a diagonal up arrow pointing right (8x8)
UP-RIGHT arrow = [
    black, black, black, black, red, red, red, red,
    black, black, black, black, black, black, red, red,
    black, black, black, black, black, red, black, red,
    black, black, black, black, red, black, black, red,
    black, black, black, red, black, black, black, black,
    black, black, red, black, black, black, black, black,
    black, red, black, black, black, black, black, black,
    red, black, black, black, black, black, black, black
]
# define a diagonal up arrow pointing left

UP-LEFT arrow = [
    red, red, red, red, black, black, black, black, 
    red, red, black, black, black, black, black, black,
    red, black, red, black, black, black, black, black,
    red, black, black, red, black, black, black, black,
    black, black, black, black, red, black, black, black,
    black, black, black, black, black, red, black, black,
    black, black, black, black, black, black, red, black,
    black, black, black, black, black, black, black, red
]

sense.set_pixels(arrow)  

# Example tyre angle
tyre_angle = 10  # Change to -10, 0, or 10 for testing

# Display arrows based on tyre angle
if tyre_angle == -10:
    sense.set_pixels(up_left_arrow)
    print("Tyre angle is -10° — displaying UP-LEFT arrow.")
elif tyre_angle == 0:
    sense.set_pixels(down_arrow)
    print("Tyre angle is 0° — displaying DOWN arrow.")
elif tyre_angle == 10:
    sense.set_pixels(up_right_arrow)
    print("Tyre angle is 10° — displaying UP-RIGHT arrow.")
else:
    sense.clear()
    print("Tyre angle outside defined range — LED matrix cleared.")
