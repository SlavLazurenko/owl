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


camera = GpsLocation(25.90737600409141, -80.13863066765238, 0)
target = GpsLocation(25.907252293090163, -80.13852248577308, 0)

directions = get_camera_direction(camera, target)

camera_center = 180

camera_rotation_angle = directions.rotation - camera_center

pantilthat.pan(camera_rotation_angle)
time.sleep(1)
