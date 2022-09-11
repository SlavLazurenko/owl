from pan_to_gps import get_camera_direction, GpsLocation
from gps3 import gps3
import pantilthat
import time
import sys

target = GpsLocation(25.907532269428554, -80.13858207192222, 5)
camera_center = int(sys.argv[1])

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
            direction = get_camera_direction(camera_location, target, camera_center)

            # print(direction)

            pantilthat.pan(direction.rotation)
            pantilthat.tilt(direction.elevation)
        except:
            print("Invalid coordinates")






