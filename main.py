import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from object_logic.high_level_functions import HighLevelCommands as hlc
from object_logic.Color import Color
from ultrasonic.ultrasonic_process import get_distance
from detect_black_area import detect_black_area


# States
LOCATE_BLACK_AREA_INIT = 0
DETECT_BLUE = 1
USER_INPUT_1 = 1.5
LOWER_FORK = 2
LIFT_FORK = 3
LOCATE_BLACK_AREA = 4
DROP_BOX = 5
USER_INPUT_2 = 5.5
DETECT_RED = 6
USER_INPUT_3 = 6.5
TRACK_RED = 7
LOWER_FORK_RED = 8
USER_INPUT_4 = 8.5
LIFT_FORK_RED = 9
DETECT_BLUE_TO_STACK = 10
STACK_RED = 11


global paused
paused = False
SERVER_ADDRESS = ('localhost', 8080)
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global paused
        if self.path == '/pause':
            paused = True
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Script paused.')
        elif self.path == '/resume':
            paused = False
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Script resumed.')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found.')

def run_server():
    httpd = HTTPServer(SERVER_ADDRESS, RequestHandler)
    print('Server running on {}:{}'.format(*SERVER_ADDRESS))
    httpd.serve_forever()

def run_main():
    # localhost:8080/pause and localhost:8080/resume using server
    # server_thread = threading.Thread(target=run_server)
    # server_thread.start()
    
    # state = LOCATE_BLACK_AREA_INIT
    state = DETECT_BLUE_TO_STACK
    counter = 0
    distance = 10000
    
    while True:
        hlc.stand_by()
        counter += 1
        print("Start of Iteration:", counter)
        if not paused:
            if state == LOCATE_BLACK_AREA_INIT:
                detect_black_area()
                state = DETECT_BLUE

            if state == DETECT_BLUE:
                if distance > 40.0:
                    distance = get_distance()
                    hlc.track_object(Color.BLUE)
                else:
                    state = LOWER_FORK

            if state == LOWER_FORK:
                hlc.lift_down()
                state = USER_INPUT_1

            if state == USER_INPUT_1:
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    hlc.prepare_to_lift()
                    state = LIFT_FORK
                else:
                    state = USER_INPUT_1

            if state == LIFT_FORK:
                hlc.lift_up()
                state = LOCATE_BLACK_AREA

            if state == LOCATE_BLACK_AREA:
                detect_black_area()
                state = DROP_BOX
                
            if state == DROP_BOX:
                hlc.lift_down()
                state = USER_INPUT_2
                
            if state == USER_INPUT_2:
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    hlc.move_backward(180)
                    hlc.lift_up()
                    state = DETECT_RED
                else:
                    state = USER_INPUT_2
                    
            if state == DETECT_RED:
                # hlc.stand_by(10)
                # area = 
                is_left, _ = hlc.check_location(Color.RED)
                
                if is_left != -1:
                    if is_left == 0:
                        while get_distance() < 60:
                            hlc.move_right(20)
                        hlc.move_right(80)
                        hlc.move_forward(90)
                        hlc.stand_by()
                    elif is_left == 1:
                        while get_distance() < 60:
                            hlc.move_left(20)
                        hlc.move_left(80)
                        hlc.move_forward(90)
                        hlc.stand_by()
                
                state = USER_INPUT_3
            
            if state == USER_INPUT_3:
                cont = input("Continue?(1/0): ")
                while cont != "1":
                    cont = input("Continue?(1/0): ")
                state = TRACK_RED
            
            if state == TRACK_RED:
                if distance > 40.0:
                    distance = get_distance()
                    hlc.track_object(Color.RED)
                else:
                    state = LOWER_FORK_RED
                    
            if state == LOWER_FORK_RED:
                hlc.lift_down()
                state = USER_INPUT_4
                
            if state == USER_INPUT_4:
                cont = input("Continue?(1/0): ")
                while cont != "1":
                    cont = input("Continue?(1/0): ")
                hlc.prepare_to_lift()
                state = LIFT_FORK_RED
            
            if state == LIFT_FORK_RED:
                hlc.lift_up()
                hlc.lift_up()
                hlc.lift_up()
                state = DETECT_BLUE_TO_STACK
            
            if state == DETECT_BLUE_TO_STACK:
                is_left = 0
                hlc.detect_blue_box(is_left)
                distance = 10000
                while distance > 3:
                    distance = get_distance()
                    hlc.track_object(Color.BLUE)
                        
                
                state = STACK_RED
            
            if state == STACK_RED:
                hlc.move_forward(2)
                hlc.lift_down()
                hlc.lift_down()
                hlc.lift_down()
                state = 255

                    

## TODO Make 2-D Array to know where the rover is and where it needs to go
## TODO replace movement timing with distance
## TODO Orientation CHecking and correction

if __name__ == '__main__':
    run_main()
    from object_logic.object_detection import detect_object
    # while True:
    #     time.sleep(1)
    # print(detect_object(Color.RED))
    # print(get_distance())
