from camera import takePicture, take_picture_from_camera
from ultrasonic_process import get_distance
from color_detection import find_zone
import serial
import time
from opencv import detect_red_objects

DO_NOTHING = 255
MOVE_FORWARD = 1
ROTATE_LEFT = 2
ROTATE_RIGHT = 3
STOP = 4

def get_command():
    picture_dir = takePicture()
    take_picture_from_camera()
    picture_dir = "resources/captured_img.jpg"
    distance = get_distance()
    distance = 5.0
    command = DO_NOTHING

    if distance < 3.0:
        command = STOP
    else:
        zone = detect_red_objects("resources/captured_img.jpg")
        if zone == 1 or zone == 4 or zone == 7:
            command = ROTATE_LEFT
        elif zone == 2 or zone == 5 or zone == 8:
            command = MOVE_FORWARD
        elif zone == 3 or zone == 6 or zone == 9:
            command = ROTATE_RIGHT
        else:
            command = DO_NOTHING
    return command

def send_command(command: int):
    ser = serial.Serial('/dev/serial0', 9600)
    ser.write(bytes[command])
    return
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
        command = get_command()
        #print(command)
