#!/usr/bin/env python

import math
import pantilthat
import time


class GpsLocation:
    def __init__(self, latitude, longitude, altitude):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude


class Direction:
    def __init__(self, rotation, elevation):
        self.rotation = rotation
        self.elevation = elevation


def get_direction(source: GpsLocation, target: GpsLocation) -> Direction:
    delta_longitude = target.longitude - source.longitude
    x = math.cos(target.latitude) * math.sin(delta_longitude)
    y = math.cos(source.latitude) * math.sin(target.latitude) \
        - math.sin(source.latitude) * math.cos(target.latitude) * math.cos(delta_longitude)

    rotation = math.atan2(x, y)

    R = 6371000

    lat1 = math.radians(source.latitude)
    lat2 = math.radians(target.latitude)
    d_lat = math.radians(target.latitude - source.latitude)
    d_lon = math.radians(target.longitude - source.longitude)

    a = math.sin(d_lat/2) * math.sin(d_lat/2) \
        + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon/2) * math.sin(d_lon/2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    d = R * c

    print(d)

    altitude_difference = target.altitude - source.altitude
    elevation = math.atan(altitude_difference / d)

    return Direction(math.degrees(rotation) % 360, math.degrees(elevation))


def get_camera_direction(camera: GpsLocation, target_object: GpsLocation, camera_center: int = 0):
    directions = get_direction(camera, target_object)

    camera_rotation_angle = (directions.rotation - camera_center) * -1
    camera_elevation_angle = directions.elevation

    return Direction(min(max(camera_rotation_angle, -90), 90), min(max(camera_elevation_angle, -90), 90))


# pantilthat.pan(min(max(camera_rotation_angle, -90), 90))
# pantilthat.tilt(min(max(camera_elevation_angle, -90), 90))
# time.sleep(1)
