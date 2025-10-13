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
# Define a diagonal up arrow pointing right (8x8)
arrow = [
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

arrow = [
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

sense.set_pixels(arrow)
