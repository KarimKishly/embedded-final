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
    def move_right(x=1):
        for _ in range(0, x):
            send_command(Actions.RIGHT)
            sleep(0.01)
    
    @staticmethod
    def move_left(x=1):
        for _ in range(0, x):
            send_command(Actions.LEFT)
            sleep(0.01)
    
    @staticmethod
    def move_forward(x=1):
        for _ in range(0, x):
            send_command(Actions.FORWARD)
            sleep(0.01)
        
    @staticmethod
    def move_backward(x=1):
        for _ in range(0, x):
            send_command(Actions.BACKWARD)
            sleep(0.01)


    @staticmethod
    def stand_by(x=1):
        for _ in range(0, x):
            send_command(Actions.NO_MOVEMENT)
            sleep(0.005)
    
    @staticmethod    
    def track_object(color: Color, img_index:int=None, min_area=None, max_area=None):
        x_center, _, area = detect_object(color, min_area, max_area, img_index)
        if x_center != -1:
            if x_center > 335: #10
                HighLevelCommands.move_right(20)
            
            elif x_center < 325: #10
                HighLevelCommands.move_left(20)
            
            else:
                HighLevelCommands.move_forward(30)
        else:
            HighLevelCommands.scan_area()
        return area


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
    def lift_up():
        for _ in range(8):
            send_command(Actions.LIFT_UP)
            sleep(0.1)
        for _ in range(5):
            send_command(Actions.NO_MOVEMENT)
            sleep(0.1)
    
    @staticmethod
    def scan_area():
        for _ in range(5):
            send_command(Actions.RIGHT)
            sleep(0.1)
        for _ in range(5):
            send_command(Actions.NO_MOVEMENT)
            sleep(0.1)
    
    @staticmethod
    def check_location(color: Color):
        centerx, _, area = detect_object(color)
        if centerx == -1:
            HighLevelCommands.scan_area_2(color)
            return -1, area
        if centerx > 320:
            return 0, area
        if centerx <= 320:
            return 1, area
        

    @staticmethod
    def scan_area_2(color: Color):
        for _ in range(15):
            HighLevelCommands.move_right(20)
            data = detect_object(color)
            if data != (-1, -1, -1):
                break
        for _ in range(15):
            HighLevelCommands.move_left(20)
            data = detect_object(color)
            if data != (-1, -1, -1):
                break
        HighLevelCommands.stand_by()
        
    @staticmethod
    def detect_blue_box(is_left):
        data = detect_object(Color.BLUE)
        print("data is:" , data)
        while data == (-1, -1, -1):
            if is_left == 0:
                HighLevelCommands.move_left(20)
            elif is_left == 1:
                HighLevelCommands.move_right(20)
            HighLevelCommands.stand_by()
            data = detect_object(Color.BLUE)
            print("data is:" , data)
        