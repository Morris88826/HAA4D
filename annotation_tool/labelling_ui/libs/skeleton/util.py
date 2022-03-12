import math
import numpy as np

def cartesian_to_spherical(origin_pos, current_pos):
    dx = current_pos[0] - origin_pos[0]
    dy = current_pos[1] - origin_pos[1]
    dz = current_pos[2] - origin_pos[2]


    r = math.sqrt(dx*dx + dy*dy + dz*dz)
    theta = math.atan2(math.sqrt(dx*dx + dy*dy), dz)
    phi = math.atan2(dy, dx)

    return r, theta, phi

def spherical_to_cartesian(origin_pos, spherical_pos):
    r = spherical_pos[0]
    theta = spherical_pos[1]
    phi = spherical_pos[2]

    x = origin_pos[0] + r*math.sin(theta)*math.cos(phi)
    y = origin_pos[1] + r*math.sin(theta)*math.sin(phi)
    z = origin_pos[2] + r*math.cos(theta)

    return x, y, z


def cartesian_to_polar(origin_pos, current_pos):
    dx = current_pos[0] - origin_pos[0]
    dy = current_pos[1] - origin_pos[1]

    r = math.sqrt(dx*dx + dy*dy)
    theta = math.atan2(dy, dx)

    return r, theta

def polar_to_cartesian(origin_pos, polar_pos):
    r = polar_pos[0]
    theta = polar_pos[1]

    x = origin_pos[0] + r*math.cos(theta)
    y = origin_pos[1] + r*math.sin(theta)

    return x, y