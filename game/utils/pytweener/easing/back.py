'''equations for easing back'''
def easeIn(t, b, c, d, s = 1.70158):
    t = t / d
    return c * t**2 * ((s+1) * t - s) + b

def easeOut (t, b, c, d, s = 1.70158):
    t = t / d - 1
    return c * (t**2 * ((s + 1) * t + s) + 1) + b

def easeInOut (t, b, c, d, s = 1.70158):
    t = t / (d * 0.5)
    s = s * 1.525
    if t < 1:
        return c * 0.5 * (t**2 * ((s + 1) * t - s)) + b
    t = t - 2
    return c / 2 * (t**2 * ((s + 1) * t + s) + 2) + b
