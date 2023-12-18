import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from object_logic.high_level_functions import HighLevelCommands as hlc
from object_logic.Color import Color
from ultrasonic.ultrasonic_process import get_distance
from detect_black_area import detect_black_area
from object_logic.object_detection import detect_object
from pygame import mixer


# States
LOCATE_BLACK_AREA_INIT = 0
INIT_SEARCH = 0.5
TRACK_BLUE = 0.75
DETECT_BLUE = 1
PREPARE_TO_LIFT = 1.5
LOWER_FORK = 2
LIFT_FORK = 3
LOCATE_BLACK_AREA = 4
DROP_BOX = 5
DETATCH_BLUE = 5.5
DETECT_RED = 6
TRACK_RED = 7
LOWER_FORK_RED = 8
PREPARE_TO_LIFT_RED = 8.5
LIFT_FORK_RED = 9
DETECT_BLUE_TO_STACK = 10
STACK_RED = 11
DETATCH_RED = 12
DETECT_GREEN = 13
TRACK_GREEN = 14
LOWER_FORK_GREEN = 15
PREPARE_TO_LIFT_GREEN = 16
LIFT_FORK_GREEN = 17
DETECT_RED_TO_STACK = 18
STACK_GREEN = 19
DETATCH_GREEN = 20
FINISH = 21

#Confirmations
CONFIRM_BLACK_AREA_INIT = 900
CONFIRM_BLACK_AREA = 901
CONFIRM_BLUE = 902
CONFIRM_LOWERED_FORK_BLUE = 903
CONFIRM_LIFTED_FORK_BLUE = 904
CONFIRM_DROP_BLUE = 905
CONFIRM_DETACHED_BLUE = 906
CONFIRM_RED = 907
CONFIRM_LOWERED_FORK_RED = 908
CONFIRM_LIFTED_FORK_RED = 909
CONFIRM_BLUE_STACK_DETECTED = 910
CONFIRM_RED_STACKED = 911
CONFIRM_RED_DETACHED = 912
CONFIRM_GREEN = 913
CONFIRM_LOWER_FORK_GREEN = 914
CONFIRM_LIFT_FORK_GREEN = 915
CONFIRM_RED_STACK_DETECTED = 916
CONFIRM_STACK_GREEN = 917


global paused
paused = False

def play_audio(file_path):
    mixer.init()
    mixer.music.load(file_path)
    mixer.music.set_volume(0.7)
    mixer.music.play()

def rover_speech(state):
    file_path = 'audio/'
    if state == CONFIRM_BLACK_AREA_INIT:
        file_path += 'black_area_detected.mp3'
    elif state == CONFIRM_BLUE:
        file_path += 'blue_box_detected.mp3'
    elif state == CONFIRM_LOWERED_FORK_BLUE:
        file_path += 'fork_down.mp3'
    elif state == CONFIRM_LIFTED_FORK_BLUE:
        file_path += 'fork_lifted.mp3'
    elif state == CONFIRM_BLACK_AREA:
        file_path += 'black_area_with_blue_box.mp3'
    elif state == CONFIRM_DROP_BLUE:
        file_path += 'drop_blue_box.mp3'
    elif state == CONFIRM_DETACHED_BLUE:
        file_path += 'blue_box_detached.mp3'
    elif state == CONFIRM_RED:
        file_path += 'red_box_detected.mp3'
    elif state == CONFIRM_LOWERED_FORK_RED:
        file_path += 'fork_down.mp3'
    elif state == CONFIRM_LIFTED_FORK_RED:
        file_path += 'fork_lifted.mp3'
    elif state == CONFIRM_BLUE_STACK_DETECTED:
        file_path += 'black_area_with_blue_box.mp3'
    elif state == CONFIRM_RED_STACKED:
        file_path += 'red_box_dropped.mp3'
    elif state == CONFIRM_RED_DETACHED:
        file_path += 'red_box_detached.mp3'
    elif state == CONFIRM_GREEN:
        file_path += 'green_box_detected.mp3'
    elif state == CONFIRM_LOWER_FORK_GREEN:
        file_path += 'fork_down.mp3'
    elif state == CONFIRM_LIFT_FORK_GREEN:
        file_path += 'fork_lifted.mp3'
    elif state == CONFIRM_RED_STACK_DETECTED:
        file_path += 'black_area_with_blue_box.mp3'
    elif state == CONFIRM_STACK_GREEN:
        file_path += 'green_box_stacked.mp3'

    # Create a new thread for playing the audio
    audio_thread = threading.Thread(target=play_audio, args=(file_path,))
    audio_thread.start()

## TODO fix after it drops BLUE, it should go to the left more or go back more because it is hitting the blue while checkign for red
# TODO move back and left after stacking red
# TODO harley sound at the beginning
# TODO add mario sound at the end
def run_main():
    # localhost:8080/pause and localhost:8080/resume using server
    # server_thread = threading.Thread(target=run_server)
    # server_thread.start()
    
    # state = LOCATE_BLACK_AREA_INIT
    state = DETECT_BLUE_TO_STACK
    counter = 0
    distance_blue = 10000
    distance_red = 10000
    distance_green = 10000
    distance_stack = 10000
    distance_stack_red = 10000
    
    while True:
        hlc.stand_by()
        counter += 1
        area = -1
        print("Start of Iteration:", counter)
        if not paused:
            if state == LOCATE_BLACK_AREA_INIT:
                print("LOCATE_BLACK_AREA_INIT")
                detect_black_area()
                state = CONFIRM_BLACK_AREA_INIT
                
            if state == CONFIRM_BLACK_AREA_INIT:
                print("CONFIRM BLACK AREA INIT:")
                rover_speech(state)
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    state = INIT_SEARCH
                else:
                    state = LOCATE_BLACK_AREA_INIT
            if state == INIT_SEARCH:
                print("INIT_SEARCH")
                hlc.lift_up()
                state = DETECT_BLUE

            if state == DETECT_BLUE:
                print("DETECT_BLUE")
                while area == -1:
                    hlc.move_left(3)
                    area = detect_object(Color.BLUE)
                hlc.stand_by()
                state = TRACK_BLUE
                    
            if state == TRACK_BLUE:
                print("TRACK_BLUE")
                distance_blue = get_distance()
                if distance_blue > 40.0:
                    #distance_blue = get_distance()
                    hlc.track_object(Color.BLUE)
                else:
                    print("Distance:", distance_blue)
                    hlc.stand_by()
                    state = CONFIRM_BLUE

            if state == CONFIRM_BLUE:
                print("CONFIRM_BLUE:")
                rover_speech(state)
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    state = LOWER_FORK
                else:
                    state = TRACK_BLUE

            if state == LOWER_FORK:
                print("LOWER_FORK")
                hlc.lift_down()
                hlc.stand_by()
                state = CONFIRM_LOWERED_FORK_BLUE
            
            if state == CONFIRM_LOWERED_FORK_BLUE:
                print("CONFIRM LOWERED FORK BLUE:")
                rover_speech(state)
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    state = PREPARE_TO_LIFT

            if state == PREPARE_TO_LIFT:
                print("PREPARE_TO_LIFT")
                hlc.prepare_to_lift()
                state = LIFT_FORK
            
            if state == LIFT_FORK:
                print("LIFT_FORK")
                hlc.lift_up()
                hlc.stand_by()
                state = CONFIRM_LIFTED_FORK_BLUE
            
            if state == CONFIRM_LIFTED_FORK_BLUE:
                print("CONFIRM LIFTED FORK BLUE:")
                rover_speech(state)
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    state = LOCATE_BLACK_AREA

            if state == LOCATE_BLACK_AREA:
                print("LOCATE_BLACK_AREA")
                detect_black_area()
                hlc.move_forward(4)
                hlc.stand_by()
                state = CONFIRM_BLACK_AREA
                
            if state == CONFIRM_BLACK_AREA:
                print("CONFIRM_BLACK_AREA:")
                rover_speech(state)
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    state = DROP_BOX
                else:
                    state = LOCATE_BLACK_AREA
                
            if state == DROP_BOX:
                print("DROP_BOX")
                hlc.lift_down()
                hlc.stand_by()
                state = CONFIRM_DROP_BLUE
                
            if state == CONFIRM_DROP_BLUE:
                print("CONFIRM_DROP_BLUE:")
                rover_speech(state)
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    state = DETATCH_BLUE
                else:
                    state = CONFIRM_DROP_BLUE
            
            if state == DETATCH_BLUE:
                print("DETATCH_BLUE")
                hlc.move_backward(18)
                hlc.lift_up()
                hlc.stand_by()
                state = CONFIRM_DETACHED_BLUE

            if state == CONFIRM_DETACHED_BLUE:
                print("CONFIRM DETACHED BLUE:")
                rover_speech(state)
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    state = DETECT_RED
                    
            if state == DETECT_RED:
                print("DETECT_RED")
                is_left, _ = hlc.check_location(Color.RED)
                
                if is_left != -1:
                    if is_left == 0:
                        while get_distance() < 60:
                            hlc.move_backward(4)
                        hlc.move_left(13)
                        hlc.move_forward(30)
                    elif is_left == 1:
                        while get_distance() < 60:
                            hlc.move_backward(4)
                        hlc.move_left(13)
                        hlc.move_forward(30)
                hlc.stand_by()
                state = TRACK_RED
            
            if state == TRACK_RED:
                print("TRACK_RED")
                distance_red = get_distance()
                if distance_red > 40.0:
                   #distance_red = get_distance()
                    hlc.track_object(Color.RED)
                else:
                    print("Distance:", distance_red)
                    hlc.stand_by()
                    state = CONFIRM_RED
                    
            if state == CONFIRM_RED:
                print("CONFIRM_RED:")
                rover_speech(state)
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    state = LOWER_FORK_RED
                else:
                    state = TRACK_RED
                    
            if state == LOWER_FORK_RED:
                print("LOWER_FORK_RED")
                hlc.lift_down()
                hlc.stand_by()
                state = CONFIRM_LOWERED_FORK_RED
                
            if state == CONFIRM_LOWERED_FORK_RED:
                print("CONFIRM LOWERED FORK RED:")
                rover_speech(state)
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    state = PREPARE_TO_LIFT_RED
            
            if state == PREPARE_TO_LIFT_RED:
                print("PREPARE_TO_LIFT_RED")
                hlc.prepare_to_lift()
                hlc.stand_by()
                state = LIFT_FORK_RED
            
            if state == LIFT_FORK_RED:
                print("LIFT_FORK_RED")
                hlc.lift_up()
                hlc.lift_up()
                hlc.stand_by()
                state = CONFIRM_LIFTED_FORK_RED

            if state == CONFIRM_LIFTED_FORK_RED:
                print("CONFIRM LIFTED FORK RED")
                rover_speech(state)
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    state = DETECT_BLUE_TO_STACK
            
            if state == DETECT_BLUE_TO_STACK:
                print("DETECT_BLUE_TO_STACK")
                is_left = 0
                hlc.detect_box_to_stack(is_left, Color.BLUE)
                while distance_stack > 25.0:
                    distance_stack = get_distance()
                    hlc.track_object(Color.BLUE)
                    hlc.stand_by()
                        
                hlc.lift_up()
                while distance_stack > 13:
                    hlc.move_forward()
                    hlc.stand_by(3)
                    distance_stack = get_distance()
                    
                hlc.stand_by()
                state = CONFIRM_BLUE_STACK_DETECTED
            
            if state == CONFIRM_BLUE_STACK_DETECTED:
                print("CONFIRM BLUE STACK DETECTED:")
                rover_speech(state)
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    state = STACK_RED
                else:
                    state = DETECT_BLUE_TO_STACK
            
            if state == STACK_RED:
                print("STACK_RED")
                hlc.move_forward()
                hlc.lift_down()
                hlc.stand_by()
                state = CONFIRM_RED_STACKED
                
            if state == CONFIRM_RED_STACKED:
                print("CONFIRM RED STACKED:")
                rover_speech(state)
                cont = input("Continue?(1/0): ")
                if cont == '1':
                    state = DETATCH_RED
            
            if state == DETATCH_RED:
                print("DETATCH_RED")
                hlc.move_backward(18)
                hlc.lift_up()
                hlc.stand_by()
                state = CONFIRM_RED_DETACHED
                
            if state == CONFIRM_RED_DETACHED:
                print("CONFIRM RED DETACHED:")
                rover_speech(state)
                cont = input("Continue?(1/0): ")
                if cont == '1':
                    state = DETECT_GREEN

            if state == DETECT_GREEN:
                print("DETECT_GREEN")
                is_left, _ = hlc.check_location(Color.GREEN, min_area = 1000)
                
                if is_left != -1:
                    if is_left == 0:
                        while get_distance() < 60:
                            hlc.move_back(4)
                        hlc.move_left(8)
                        hlc.move_forward(9)
                        hlc.stand_by()
                    elif is_left == 1:
                        while get_distance() < 60:
                            hlc.move_back(4)
                        hlc.move_left(8)
                        hlc.move_forward(9)
                        hlc.stand_by()
                
                state = TRACK_GREEN
            
            if state == TRACK_GREEN:
                print("TRACK_GREEN")
                distance_green = get_distance()
                if distance_green > 40.0:
                    #distance_green = get_distance()
                    hlc.track_object(Color.GREEN, min_area = 1000)
                else:
                    state = CONFIRM_GREEN
                    
            if state == CONFIRM_GREEN:
                print("CONFIRM GREEN")
                rover_speech(state)
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    state = LOWER_FORK_GREEN
                else:
                    state = TRACK_GREEN
            
            if state == LOWER_FORK_GREEN:
                print("LOWER_FORK_GREEN")
                hlc.lift_down()
                state = CONFIRM_LOWER_FORK_GREEN
                
            if state == CONFIRM_LOWER_FORK_GREEN:
                print("CONFIRM LOWER FORK GREEN")
                rover_speech(state)
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    state = PREPARE_TO_LIFT_GREEN
           #####################################################################    
            if state == PREPARE_TO_LIFT_GREEN:
                print("PREPARE_TO_LIFT_GREEN")
                hlc.prepare_to_lift()
                state = LIFT_FORK_GREEN
            
            if state == LIFT_FORK_GREEN:
                print("LIFT_FORK_GREEN")
                hlc.lift_up()
                hlc.lift_up()
                state = DETECT_RED_TO_STACK
                
            if state == CONFIRM_LIFT_FORK_GREEN:
                print("CONFIRM LIFT FORK GREEN")
                rover_speech(state)
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    state = DETECT_RED_TO_STACK
            
            if state == DETECT_RED_TO_STACK:
                print("DETECT_RED_TO_STACK")
                is_left = 0
                hlc.detect_box_to_stack(is_left, Color.RED)
                distance_stack_red = 10000
                while distance_stack_red > 25.0:
                    distance_stack_red = get_distance()
                    hlc.track_object(Color.RED)
                        
                hlc.lift_up()
                while distance_stack_red > 5:
                    hlc.move_forward()
                    hlc.stand_by(3)
                    distance_stack_red = get_distance()
                
                state = CONFIRM_RED_STACK_DETECTED
            
            if state == CONFIRM_RED_STACK_DETECTED:
                print("CONFIRM RED STACK DETECTED")
                rover_speech(state)
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    state = STACK_GREEN
                else:
                    state = DETECT_RED_TO_STACK
            
            if state == STACK_GREEN:
                print("STACK_GREEN")
                hlc.move_forward()
                hlc.lift_down()
                hlc.lift_down()
                hlc.lift_down()
                state = CONFIRM_STACK_GREEN
                
            if state == CONFIRM_STACK_GREEN:
                print("CONFIRM STACK GREEN")
                rover_speech(state)
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    state = DETATCH_GREEN
            
            if state == DETATCH_GREEN:
                print("DETATCH_GREEN")
                hlc.move_backward(18)
                hlc.lift_up()
                state = FINISH
            
            if state == FINISH:
                print("FINISH")
                print("Program Over...")
                break
                
            

                    

## TODO Make 2-D Array to know where the rover is and where it needs to go
## TODO replace movement timing with distance
## TODO Orientation CHecking and correction

if __name__ == '__main__':
    run_main()
    from object_logic.object_detection import detect_object
    # while True:
    #     print(detect_object(Color.GREEN, min_area = 1000, max_area = 300000))
    # print(get_distance())
