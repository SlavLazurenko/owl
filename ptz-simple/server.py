import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Lock
from threading import Thread
from gps3 import gps3
import pantilthat
import os

from pan_to_gps import GpsLocation, get_camera_direction

hostName = os.environ.get('HOST', 'localhost')
serverPort = os.environ.get('PORT', '8080')

target_location = GpsLocation(0, 0, 0)

class MyServer(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        return super(MyServer, self).end_headers()

    def do_POST(self):
        global target_location
        global lock
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        print("POST request,\nPath: {}\nHeaders:\n{}\n\nBody:\n{}\n".format(str(self.path), str(self.headers),
                                                                            post_data.decode('utf-8')))

        try:
            j = json.loads(post_data.decode('utf-8'))
            with lock:
                target_location.latitude = j['lat']
                target_location.longitude = j['lng']
                target_location.altitude = j['alt']

            print("Request ", target_location)
            self.send_response(200)
            # self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'text/html')
        except:
            self.send_response(500)
            # self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'text/html')

        self.end_headers()


def test_task(lock, target_location: GpsLocation):
    print('waiting for data')
    while True:
        with lock:
            print(target_location)
        time.sleep(1)

# work function
def task(lock, target_location: GpsLocation):
    # acquire the lock
    camera_center = float(os.environ.get('CAMERA_DIRECTION_DEGREES', '0'))

    gps_socket = gps3.GPSDSocket()
    data_stream = gps3.DataStream()
    gps_socket.connect()
    gps_socket.watch()

    print('waiting for data')

    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            camera_location = GpsLocation(data_stream.TPV['lat'], data_stream.TPV['lon'], data_stream.TPV['alt'])
            print(camera_location)

            try:
                with lock:
                    direction = get_camera_direction(camera_location, target_location, camera_center)

                print(direction)

                pantilthat.pan(direction.rotation)
                pantilthat.tilt(direction.elevation)
            except:
                print("Invalid coordinates")


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    lock = Lock()

    Thread(target=task, args=(lock, target_location)).start()

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
