from object_logic.object_detection import detect_object
from object_logic.Color import Color
from object_logic.actions import Actions
import serial
from time import sleep

def send_command(command: int):
    ser = serial.Serial('/dev/serial0', 9600)
    ser.write(bytes([command]))
    print(command)
    return

class HighLevelCommands():
    @staticmethod
    def stand_by():
        send_command(Actions.NO_MOVEMENT)
        sleep(0.005)
    
    @staticmethod    
    def track_object(color: Color, img_index:int=None):
        x_center = detect_object(color, img_index)
        print("Center of Object:", x_center)
        
        if x_center != -1:
            if x_center[0] > 325: #10
                movement = Actions.RIGHT
                delay = 0.2
            
            elif x_center[0] < 305: #10
                movement = Actions.LEFT
                delay = 0.2
            
            else:
                movement = Actions.FORWARD
                delay = 0.3
        else:
            movement = Actions.NO_MOVEMENT
            delay = 0
            
        send_command(movement)
        sleep(delay)

    @staticmethod            
    def lift_down():
        for _ in range(6):
            send_command(Actions.LIFT_DOWN)
            sleep(0.1)
        for _ in range(5):
            send_command(Actions.NO_MOVEMENT)
            sleep(0.1)
  
    @staticmethod
    def prepare_to_lift():
        for _ in range(20):
            send_command(Actions.FORWARD)
            sleep(0.1)
        for _ in range(5):
            send_command(Actions.NO_MOVEMENT)
            sleep(0.1)


    @staticmethod
    def lift_fork():
        for _ in range(22):
            send_command(Actions.LIFT_UP)
            sleep(0.1)
        for _ in range(5):
            send_command(Actions.NO_MOVEMENT)
            sleep(0.1)

