from object_logic.Color import Color
from object_logic.actions import Actions
from object_logic.object_detection import detect_object
from object_logic.high_level_functions import send_command, HighLevelCommands as hlc
from time import sleep

def detect_black_area():
    while detect_object(Color.BLACK) == -1:
        for _ in range(2):
            send_command(Actions.RIGHT)
            sleep(0.1)
            send_command(Actions.NO_MOVEMENT)
            sleep(0.1)
    while detect_object(Color.BLACK) != -1:
        hlc.track_object(Color.BLACK)
        hlc.stand_by()
    

if __name__ == "__main__":
    detect_black_area()