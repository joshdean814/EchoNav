from sense_hat import SenseHat
sense = SenseHat()

red = (255, 0, 0)
black = (0, 0, 0)

# Define a down arrow (8x8)
arrow = [
    black, black, black, red,   red,   black, black, black,
    black, black, black, red,   red,   black, black, black,
    black, black, black, red,   red,   black, black, black,
    black, black, black, red,   red,   black, black, black,
    red,   black, black, red,   red,   black, black, red,
    black, red,   black, red,   red,   black, red,   black,
    black, black, red,   red,   red,   red,   black, black,
    black, black, black, red,   red,   black, black, black
]

sense.set_pixels(arrow)
