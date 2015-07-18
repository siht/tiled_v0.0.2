'''equations for easing strong'''
def easeIn(t, b, c, d):
    return c * (t/d)**5 + b

def easeOut(t, b, c, d):
    return c * ((t / d - 1)**5 + 1) + b

def easeInOut(t, b, c, d):
    t = t / (d * 0.5)
    if t < 1:
        return c * 0.5 * t**5 + b
    t = t - 2
    return c * 0.5 * (t**5 + 2) + b
