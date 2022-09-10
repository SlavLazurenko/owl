import sys
from gps3 import gps3
import pantilthat
import time
import math
from pan_to_gps import GpsLocation

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()


def get_cords():
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
    return GpsLocation(data_stream.TPV['lat'], data_stream.TPV['lon'], data_stream.TPV['alt'])


def look_at_object():
    rotation = ()
    elevation = ()

    pantilthat.pan(rotation)
    pantilthat.tilt(elevation)
    time.sleep(0.05)




