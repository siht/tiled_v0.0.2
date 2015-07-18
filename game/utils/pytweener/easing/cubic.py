'''equations for easing cubic'''
def easeIn (t, b, c, d):
    t = t / d
    return c * t**3 + b

def easeOut (t, b, c, d):
    t = t / d - 1
    return c * (t**3 + 1) + b

def easeInOut (t, b, c, d):
    t = t / (d * 0.5)
    if t < 1:
        return c * 0.5 * t**3 + b
    t = t - 2
    return c * 0.5 * (t**3 + 2) + b
