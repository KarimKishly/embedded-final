import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import serial
from object_logic.object_tracking import track_object
from object_logic.Color import Color
from ultrasonic.ultrasonic_processbuilder import read_sensor

# States
DETECT_RED = 0
LIFT_FORK = 1
LOCATE_BLACK_AREA = 2


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

def send_command(command: int):
    # ser = serial.Serial('/dev/serial0', 9600)   #TODO uncomment
    # ser.write(bytes[command])
    print(command)
    return

if __name__ == '__main__':
    # localhost:8080/pause and localhost:8080/resume using server
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    state = DETECT_RED
    counter = 0
    while True:
        time.sleep(0.5)
        counter += 1
        print("Start of Iteration:", counter)
        if not paused:
            if state == DETECT_RED:
                # distance = read_sensor()    #TODO uncomment
                distance = 15
                
                if distance > 10.0:
                    action = track_object(Color.GREEN)
                    send_command(action)
                else:
                    state = LIFT_FORK

            if state == LIFT_FORK:
                send_command(LIFT_UP)
                time.sleep(1.5)
                send_command(STOP_LIFT)
                state = LOCATE_BLACK_AREA

            if state == LOCATE_BLACK_AREA:
                track_object(Color.BLACK)
