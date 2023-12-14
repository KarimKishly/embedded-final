from color.box_tracker import detect_box_center
from color.Color import Color
import random

NO_MOVEMENT = 255
FORWARD = 1
LEFT = 2
RIGHT = 3

def track_red_box():
    x_center = detect_box_center(Color.RED)
    print(x_center)
    if x_center != -1:
        # if center of box > center of image + 10 pixels
        if x_center > 250: # tune this number as you see fit
            movement = LEFT
        # if center of box < center of image - 10 pixels
        elif x_center < 230: # tune this number as you see fit
            movement = RIGHT
        else:
            movement = FORWARD
    else:
        # if box not found, rotate in a random direction until box is found
        movement = random.choice([LEFT, RIGHT])
    return movement

if __name__ == '__main__':
    while True:
        x = track_red_box()
        if x == FORWARD:
            print("FORWARD")
        if x == LEFT:
            print("LEFT")
        if x == RIGHT:
            print("RIGHT")

