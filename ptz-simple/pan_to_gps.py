#!/usr/bin/env python

import math
import pantilthat
import time


class GpsLocation:
    def __init__(self, latitude, longitude, altitude):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def __str__(self):
        return 'Altitude = ' + str(self.altitude) + ', Latitude = ' + str(self.latitude) + ', Longitude = ' + str(self.longitude)


class Direction:
    def __init__(self, rotation, elevation):
        self.rotation = rotation
        self.elevation = elevation

    def __str__(self):
        return 'Rotation = ' + str(self.rotation) + ', Elevation = ' + str(self.elevation)


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

    altitude_difference = target.altitude - source.altitude
    elevation = math.atan(altitude_difference / d)

    direction = Direction(math.degrees(rotation) % 360, math.degrees(elevation))
    print(direction)
    return direction


def get_camera_direction(camera: GpsLocation, target_object: GpsLocation, camera_center: int = 0):
    directions = get_direction(camera, target_object)

    camera_rotation_angle = directions.rotation
    if camera_rotation_angle >= 180:
        camera_rotation_angle = camera_rotation_angle - 360

    camera_rotation_angle = (camera_rotation_angle - camera_center) * -1
    camera_elevation_angle = (directions.elevation -23)* -1

    return Direction(min(max(camera_rotation_angle, -90), 90), min(max(camera_elevation_angle, -90), 90))

