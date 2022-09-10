#!/usr/bin/env python

import math
import pantilthat
import time


class GpsLocation:
    def __init__(self, latitude, longitude, altitude):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude


class CameraDirection:
    def __init__(self, rotation, elevation):
        self.rotation = rotation
        self.elevation = elevation


def get_camera_direction(camera: GpsLocation, target: GpsLocation) -> CameraDirection:
    delta_longitude = target.longitude - camera.longitude
    x = math.cos(target.latitude) * math.sin(delta_longitude)
    y = math.cos(camera.latitude) * math.sin(target.latitude) - math.sin(camera.latitude) * math.cos(target.latitude) * math.cos(
        delta_longitude)

    rotation = math.atan2(x, y)
    elevation = 0

    return CameraDirection(math.degrees(rotation) % 380, elevation)


camera = GpsLocation(25.90735990503165, -80.13862756341351, 0)
target = GpsLocation(25.907166827337466, -80.13907274279559, 0)

directions = get_camera_direction(camera, target)

camera_center = 180

camera_rotation_angle = (directions.rotation - camera_center) * -1

print(camera_rotation_angle)


pantilthat.pan(min(max(camera_rotation_angle, -90), 90))
# pantilthat.pan(90)
time.sleep(1)
