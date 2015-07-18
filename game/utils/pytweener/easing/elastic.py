'''equations for easing elastic'''
import math
def easeIn (t, b, c, d, a = 0, p = 0):
    if t==0: return b
    t = t / d            
    if t == 1: return b+c
    if not p: p = d * .3;
    if not a or a < abs(c):
        a = c
        s = p / 4
    else:
        s = p / (2 * math.pi) * math.asin(c / a)
    t = t - 1            
    return - (a * (2**(10 * t)) * math.sin((t*d-s) * (2 * math.pi) / p)) + b

def easeOut (t, b, c, d, a = 0, p = 0):
    if t == 0: return b
    t = t / d
    if (t == 1): return b + c
    if not p: p = d * .3;
    if not a or a < abs(c):
        a = c
        s = p / 4
    else:
        s = p / (2 * math.pi) * math.asin(c / a)
    return a * (2**(-10 * t)) * math.sin((t * d - s) * (2 * math.pi) / p) + c + b

def easeInOut (t, b, c, d, a = 0, p = 0):
    if t == 0: return b
    t = t / (d * 0.5)
    if t == 2: return b + c
    if not p: p = d * (.3 * 1.5)
    if not a or a < abs(c):
        a = c
        s = p / 4
    else:
        s = p / (2 * math.pi) * math.asin(c / a)
    if (t < 1):
        t = t - 1
        return -.5 * (a *(2**(10 * t)) * math.sin((t * d - s) * (2 * math.pi) / p)) + b
    t = t - 1
    return a * (2**(-10 * t)) * math.sin((t * d - s) * (2 * math.pi) / p) * .5 + c + b
