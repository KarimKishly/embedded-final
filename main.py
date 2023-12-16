import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from object_logic.high_level_functions import HighLevelCommands as hlc
from object_logic.Color import Color
from ultrasonic.ultrasonic_process import get_distance


# States
DETECT_BLUE = 0
USER_INPUT = 0.5
LOWER_FORK = 1
LIFT_FORK = 2
LOCATE_BLACK_AREA = 3


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



if __name__ == '__main__':
    # localhost:8080/pause and localhost:8080/resume using server
    # server_thread = threading.Thread(target=run_server)
    # server_thread.start()
    state = DETECT_BLUE
    counter = 0
    distance = 10000
    
    while True:
        hlc.stand_by()
        counter += 1
        print("Start of Iteration:", counter)
        if not paused:
            if state == DETECT_BLUE:
                # if distance > 50.0:
                #     if counter == 3:
                #         distance = get_distance()
                #         counter = 0
                if distance > 40.0:
                    distance = get_distance()
                    hlc.track_object(Color.RED)
                else:
                    state = LOWER_FORK

            if state == LOWER_FORK:

                hlc.lift_down()
                state = USER_INPUT

            if state == USER_INPUT:
                cont = input("Continue?(1/0): ")
                if cont == "1":
                    hlc.prepare_to_lift()
                    state = LIFT_FORK
                else:
                    state = USER_INPUT

            if state == LIFT_FORK:

                hlc.lift_fork()
                state = LOCATE_BLACK_AREA


            if state == LOCATE_BLACK_AREA:
                # track_object(Color.BLACK)
                pass
