from object_logic.Color import Color
from object_logic.actions import Actions
from object_logic.object_detection import detect_object
from object_logic.high_level_functions import send_command, HighLevelCommands as hlc
from time import sleep

def detect_black_area():
    data = detect_object(Color.BLACK, min_area=10000, max_area=300000)
    print("data is:" , data)
    while data == (-1, -1, -1):
        hlc.scan_area()
        hlc.stand_by()
        data = detect_object(Color.BLACK, min_area=10000, max_area=300000)
        print("data is:" , data)
    while data != (-1, -1, -1):
        hlc.track_object(Color.BLACK, min_area=10000, max_area=300000)
        hlc.stand_by()
        data = detect_object(Color.BLACK, min_area=10000, max_area=300000)
        print("data is:" , data)
    
    

    
    

if __name__ == "__main__":
    detect_black_area()