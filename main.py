import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from object_logic.high_level_functions import HighLevelCommands as hlc
from object_logic.Color import Color
from ultrasonic.ultrasonic_process import get_distance


# States
DETECT_BLUE = 0
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
                
                if counter == 3:
                    distance = get_distance()
                    counter = 0
                
                if distance > 50.0:
                    hlc.track_object(Color.BLUE)
                else:
                    state = LOWER_FORK

            if state == LOWER_FORK:

                hlc.prepare_to_lift()
                state = LIFT_FORK

            if state == LIFT_FORK:

                hlc.lift_fork()
                state = LOCATE_BLACK_AREA


            if state == LOCATE_BLACK_AREA:
                # track_object(Color.BLACK)
                pass
