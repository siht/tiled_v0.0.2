'''equations for easing sine'''
import math
def easeIn (t, b, c, d):
    return -c * math.cos(t / d * (math.pi / 2)) + c + b

def easeOut (t, b, c, d):
    return c * math.sin(t / d * (math.pi / 2)) + b

def easeInOut (t, b, c, d):
    return -c * 0.5 * (math.cos(math.pi * t / d) - 1) + b
