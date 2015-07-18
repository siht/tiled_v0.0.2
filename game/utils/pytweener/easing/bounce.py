'''equations for easing bounce'''
def easeOut (t, b, c, d):
    t = t / d
    if t < 1 / 2.75:
        return c * (7.5625 * t**2) + b
    elif t < 2 / 2.75:
        t = t - 1.5 / 2.75
        return c * (7.5625 * t**2 + 0.75) + b
    elif t < 2.5 / 2.75:
        t = t - 2.25 / 2.75
        return c * (7.5625 * t**2 + .9375) + b
    else:
        t = t - 2.625 / 2.75
        return c * (7.5625 * t**2 + 0.984375) + b

def easeIn (t, b, c, d):
    return c - easeOut(d-t, 0, c, d) + b

def easeInOut (t, b, c, d):
    if t < d * 0.5:
        return easeIn(t * 2, 0, c, d) * .5 + b
    return easeOut(t * 2 -d, 0, c, d) * .5 + c*.5 + b
