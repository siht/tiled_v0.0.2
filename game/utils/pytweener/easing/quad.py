'''equations for easing quad'''
def easeIn (t, b, c, d):
    t = t / d
    return c * t**2 + b

def easeOut (t, b, c, d):
    t = t / d
    return -c * t * (t-2) + b

def easeInOut (t, b, c, d):
    t = t / (d * 0.5)
    if t < 1:
        return c * 0.5 * t**2 + b
    t = t - 1
    return -c * 0.5 * (t * (t - 2) - 1) + b
