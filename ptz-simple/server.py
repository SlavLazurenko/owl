import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Lock
from threading import Thread
from gps3 import gps3
import pantilthat

from pan_to_gps import GpsLocation, get_camera_direction

hostName = "localhost"
serverPort = 8080

target_location = GpsLocation(0, 0, 0)


class MyServer(BaseHTTPRequestHandler):
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
                target_location.latitude = j['latitude']
                target_location.longitude = j['longitude']
                target_location.altitude = j['altitude']

            print("Request ", target_location)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
        except:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')

        self.end_headers()


# work function
def task(lock, target_location: GpsLocation):
    # acquire the lock
    camera_center = 35

    gps_socket = gps3.GPSDSocket()
    data_stream = gps3.DataStream()
    gps_socket.connect()
    gps_socket.watch()

    print('waiting for data')
    # while True:
    #     with lock:
    #         print(target_location)
    #     time.sleep(1)

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
