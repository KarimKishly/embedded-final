from object_logic.object_detection import detect_object
from object_logic.Color import Color
import random

# Actions
# NO_MOVEMENT = 0   #TODO uncomment
# FORWARD = 1
# BACKWARD = 2
# RIGHT = 5
# LEFT = 6
# LIFT_UP = 7
# LIFT_DOWN = 8

NO_MOVEMENT = "No Movement"  #TODO comment
FORWARD = "Forward"
BACKWARD = "Backward"
RIGHT = "Right"
LEFT = "Left"
LIFT_UP = "Lift Up"
LIFT_DOWN = "Lift Down"

def track_object(color: Color, img_index:int=None):
    x_center = detect_object(color, img_index)
    print(x_center)
    if x_center != -1:
        # if center of box > center of image + 10 pixels
        if x_center > 200: # tune this number as you see fit
            movement = RIGHT
        # if center of box < center of image - 10 pixels
        elif x_center < 100: # tune this number as you see fit
            movement = LEFT
        else:
            movement = FORWARD
    else:
        # if box not found, rotate in a random direction until box is found
        # movement = random.choice([LEFT, RIGHT]) ## this will make the rover go psycho, i suggest we keep a method that is just for finding (or refinding) the red box
        movement = NO_MOVEMENT
    return movement

if __name__ == '__main__':
    while True:
        x = track_object(Color.RED)
        if x == FORWARD:
            print("FORWARD")
        if x == LEFT:
            print("LEFT")
        if x == RIGHT:
            print("RIGHT")

