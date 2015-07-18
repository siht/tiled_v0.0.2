'''equations for easing circ'''
import math
def easeIn (t, b, c, d):
    t = t / d
    return -c * (math.sqrt(1 - t**2) - 1) + b

def easeOut (t, b, c, d):
    t = t / d - 1
    return c * math.sqrt(1 - t**2) + b

def easeInOut (t, b, c, d):
    t = t / (d * 0.5)
    if t < 1:
        return -c * 0.5 * (math.sqrt(1 - t**2) - 1) + b
    t = t - 2
    return c*0.5 * (math.sqrt(1 - t**2) + 1) + b
