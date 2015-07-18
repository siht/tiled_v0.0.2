'''equations for easing expo'''
def easeIn(t, b, c, d):
    if t == 0:
        return b
    else:
        return c * (2**(10 * (t / d - 1))) + b - c * 0.001

def easeOut(t, b, c, d):
    if t == d:
        return b + c
    else:
        return c * (-(2**(-10 * t / d)) + 1) + b

def easeInOut(t, b, c, d):
    if t==0:
        return b
    elif t==d:
        return b+c
    t = t / (d * 0.5)
    if t < 1:
        return c * 0.5 * (2**(10 * (t - 1))) + b
    return c * 0.5 * (-(2**(-10 * (t - 1))) + 2) + b
