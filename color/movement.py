from red_box import detect_red_box
from blue_box import detect_blue_box
from green_box import detect_green_box

NO_MOVEMENT = -1
FORWARD = 0
LEFT = 1
RIGHT = 2

def move():
    movement = NO_MOVEMENT
    x = detect_red_box()
    if x != -1:
        if x > 250:
            movement = LEFT
        elif x < 230:
            movement = RIGHT
        else:
            movement = FORWARD
    else:
        movement = NO_MOVEMENT
    return movement

if __name__ == '__main__':
    while True:
        print(move())

