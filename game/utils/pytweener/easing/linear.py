'''equations for easing linear'''
def easeNone(t, b, c, d):
    return c * t / d + b

def easeIn(t, b, c, d):
    return c * t / d + b

def easeOut(t, b, c, d):
    return c * t / d + b

def easeInOut(t, b, c, d):
    return c * t / d + b
