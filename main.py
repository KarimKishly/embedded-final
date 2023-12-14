import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import serial

from color.movement import track_red_box
from ultrasonic.ultrasonic_processbuilder import read_sensor

# States
DETECT_RED = 0
LIFT_FORK = 1
LOCATE_BLACK_AREA = 2

# Actions
NO_MOVEMENT = 255
FORWARD = 0
LEFT = 1
RIGHT = 2
STOP_LIFT = 6
LIFT_UP = 7
LIFT_DOWN = 8

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
    ser = serial.Serial('/dev/serial0', 9600)
    ser.write(bytes[command])
    return

if __name__ == '__main__':
    # localhost:8080/pause and localhost:8080/resume using server
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    state = DETECT_RED
    while True:
        if not paused:
            if state == DETECT_RED:
                distance = read_sensor()
                if distance < 10.0:
                    action = track_red_box()
                    send_command(action)
                else:
                    state = LIFT_FORK

            if state == LIFT_FORK:
                send_command(LIFT_UP)
                time.sleep(1.5)
                send_command(STOP_LIFT)
                state = LOCATE_BLACK_AREA

            if state == LOCATE_BLACK_AREA:
                track_red_box()
