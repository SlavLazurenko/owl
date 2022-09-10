from get_data import get_cords
from pan_to_gps import get_camera_direction, GpsLocation
import pantilthat
import time

target = GpsLocation(25.907620255792594, -80.13785843477541, 5)
camera_center = 0

direction = get_camera_direction(get_cords(), target, camera_center)

pantilthat.pan(direction.rotation)
pantilthat.tilt(direction.elevation)
time.sleep(1)



