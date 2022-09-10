from pan_to_gps import get_camera_direction, GpsLocation
import pantilthat
import time

camera = GpsLocation(25.90742603762201, -80.13840962874826, 10)
target = GpsLocation(25.907620255792594, -80.13785843477541, 5)
camera_center = 180

direction = get_camera_direction(camera, target, camera_center)

print(direction.rotation)
print(direction.elevation)

pantilthat.pan(direction.rotation)
pantilthat.tilt(direction.elevation)
time.sleep(1)
