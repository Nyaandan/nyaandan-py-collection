import math

def vector_to_angle(x, y):
    theta = math.atan2(y, x)
    value = math.degrees(theta)
    return value