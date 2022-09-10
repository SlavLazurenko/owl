from pan_to_gps import get_camera_direction, GpsLocation

camera = GpsLocation(25.90742603762201, -80.13840962874826, 10)
target = GpsLocation(25.907620255792594, -80.13785843477541, 5)
camera_center = 180

directions = get_camera_direction(camera, target, camera_center)

print(directions.rotation)
print(directions.elevation)
