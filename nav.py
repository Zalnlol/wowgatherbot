import math
import numpy as np

def get_nav_turn_angle(nav_loc, w=300, h=300):
    w_center = w // 2
    dx = nav_loc[0] - w_center
    dy = nav_loc[1] - h

    angle = math.atan2(dx, dy) % math.pi
    if angle > math.pi / 2.0:
        angle -= math.pi
    return angle


def get_nav_elevation_angle(nav_loc, w=300, h=300):
    h_center = h // 2
    dx = nav_loc[0] - w
    dy = nav_loc[1] - h_center
    angle = math.atan2(dy, dx) % math.pi
    if angle > math.pi / 2.0:
        angle -= math.pi
    return angle