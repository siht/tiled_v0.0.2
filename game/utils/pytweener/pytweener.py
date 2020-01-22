# pyTweener
#
# Tweening functions for python
#
# Heavily based on caurina Tweener: http://code.google.com/p/tweener/
#
# Released under M.I.T License - see above url
# Python version by Ben Harling 2009 
# mod by me 16 -7 -2015
from . import easing

class NoArgumentError(BaseException): pass

class Tweener(object):
    def __init__(self, duration=0.5, tween=None):
        """Tweener
        This class manages all active tweens, and provides a factory for
        creating and spawning tween motions."""
        self.currentTweens = []
        self.defaultTweenType = tween or easing.cubic.easeInOut
        self.defaultDuration = duration or 1.0

    def hasTweens(self):
        return len(self.currentTweens) > 0

    def addTween(self, obj, **kwargs):
        """ addTween( object, **kwargs) -> tweenObject or False
            Example:
            tweener.addTween( myRocket, throttle=50, setThrust=400, tweenTime=5.0, tweenType=tweener.OUT_QUAD )
            You must first specify an object, and at least one property or function with a corresponding
            change value. The tween will throw an error if you specify an attribute the object does
            not possess. Also the data types of the change and the initial value of the tweened item
            must match. If you specify a 'set' -type function, the tweener will attempt to get the
            starting value by call the corresponding 'get' function on the object. If you specify a 
            property, the tweener will read the current state as the starting value. You add both 
            functions and property changes to the same tween.
            in addition to any properties you specify on the object, these keywords do additional
            setup of the tween.
            tweenTime = the duration of the motion
            tweenType = one of the predefined tweening equations or your own function
            onCompleteFunction = specify a function to call on completion of the tween
            onUpdateFunction = specify a function to call every time the tween updates
            tweenDelay = specify a delay before starting.
            """
        if "tweenTime" in kwargs:
            t_time = kwargs.pop("tweenTime")
        else: t_time = self.defaultDuration

        if "tweenType" in kwargs:
            t_type = kwargs.pop("tweenType")
        else: t_type = self.defaultTweenType

        if "onCompleteFunction" in kwargs:
            t_completeFunc = kwargs.pop("onCompleteFunction")
        else: t_completeFunc = None

        if "onUpdateFunction" in kwargs:
            t_updateFunc = kwargs.pop("onUpdateFunction")
        else: t_updateFunc = None

        if "tweenDelay" in kwargs:
            t_delay = kwargs.pop("tweenDelay")
        else: t_delay = 0

        tw = Tween( obj, t_time, t_type, t_completeFunc, t_updateFunc, t_delay, **kwargs )
        if tw:    
            self.currentTweens.append( tw )
        return tw

    def removeTween(self, tweenObj):
        if tweenObj in self.currentTweens:
            tweenObj.complete = True
            #self.currentTweens.remove( tweenObj )

    def getTweensAffectingObject(self, obj):
        """Get a list of all tweens acting on the specified object
        Useful for manipulating tweens on the fly"""
        tweens = []
        for t in self.currentTweens:
            if t.target is obj:
                tweens.append(t)
        return tweens

    def removeTweeningFrom(self, obj):
        """Stop tweening an object, without completing the motion
        or firing the completeFunction"""
        for t in self.currentTweens:
            if t.target is obj:
                t.complete = True

    def finish(self):
        #go to last frame for all tweens
        for t in self.currentTweens:
            t.update(t.duration)
        self.currentTweens = []

    def update(self, timeSinceLastFrame):
        removable = []
        for t in self.currentTweens:
            t.update(timeSinceLastFrame)
            if t.complete:
                removable.append(t)
        for t in removable:
            self.currentTweens.remove(t)

class Tween(object):
    def __init__(self, obj, tduration, tweenType, completeFunction, updateFunction, delay, **kwargs):
        """Tween object:
            Can be created directly, but much more easily using Tweener.addTween( ... )
            """
        self.duration = tduration
        self.delay = delay
        self.target = obj
        self.tween = tweenType
        self.tweenables = kwargs
        self.delta = 0
        self.completeFunction = completeFunction
        self.updateFunction = updateFunction
        self.complete = False
        self.tProps = []
        self.tFuncs = []
        self.paused = self.delay > 0
        self.decodeArguments()

    def decodeArguments(self):
        """Internal setup procedure to create tweenables and work out
           how to deal with each"""
        if len(self.tweenables) == 0:
            raise NoArgumentError("No Tweenable properties or functions defined")
        for k, v in self.tweenables.items():
        # check that its compatible
            if not hasattr(self.target, k):
                raise AttributeError("{} has no function {}".format(self.target, k))
            prop = func = False
            startVal = 0
            newVal = v
            if not callable(getattr(self.target, k)):
                # variables and properties
                startVal = getattr(self.target, k)
                prop = k
            else:
                # methods or functions
                func = getattr(self.target, k)
                funcName = k
            if func:
                try:
                    getFunc = getattr(self.target, funcName.replace("set", "get"))
                    startVal = getFunc()
                except:
                    # no start value, assume its 0
                    # but make sure the start and change
                    # dataTypes match :)
                    startVal = newVal * 0
                tweenable = Tweenable( startVal, newVal-startVal)
                newFunc = [ k, func, tweenable]
                #setattr(self, funcName, newFunc[2])
                self.tFuncs.append(newFunc)
            if prop:
                tweenable = Tweenable(startVal, newVal - startVal)    
                newProp = [k, prop, tweenable]
                self.tProps.append(newProp)  

    def pause(self, numSeconds=-1):
        """Pause this tween
            do tween.pause( 2 ) to pause for a specific time
            or tween.pause() which pauses indefinitely."""
        self.paused = True
        self.delay = numSeconds

    def resume(self):
        """Resume from pause"""
        if self.paused:
            self.paused = False

    def update(self, ptime):
        """Update this tween with the time since the last frame
            if there is an update function, it is always called
            whether the tween is running or paused"""
        if self.complete:
            return
        if self.paused:
            if self.delay > 0:
                self.delay = max( 0, self.delay - ptime )
                if self.delay == 0:
                    self.paused = False
                    self.delay = -1
                if self.updateFunction:
                    self.updateFunction()
            return
        self.delta = min(self.delta+ptime, self.duration)
        for propName, prop, tweenable in self.tProps:
            setattr(self.target,
                    propName,
                    self.tween(self.delta, tweenable.startValue, tweenable.change, self.duration))
        for funcName, func, tweenable in self.tFuncs:
            func(self.tween(self.delta, tweenable.startValue, tweenable.change, self.duration))
        if self.delta == self.duration:
            self.complete = True
            if self.completeFunction:
                self.completeFunction()
        if self.updateFunction:
            self.updateFunction()

    def getTweenable(self, name):
        """Return the tweenable values corresponding to the name of the original
        tweening function or property. 
        Allows the parameters of tweens to be changed at runtime. The parameters
        can even be tweened themselves!
        eg:
        # the rocket needs to escape!! - we're already moving, but must go faster!
        twn = tweener.getTweensAffectingObject( myRocket )[0]
        tweenable = twn.getTweenable( "thrusterPower" )
        tweener.addTween( tweenable, change=1000.0, tweenTime=0.4, tweenType=tweener.IN_QUAD )
        """
        ret = None
        for n, f, t in self.tFuncs:
            if n == name:
                ret = t
                return ret
        for n, p, t in self.tProps:
            if n == name:
                ret = t
                return ret
        return ret

    def Remove(self):
        """Disables and removes this tween
            without calling the complete function"""
        self.complete = True

class Tweenable(object):
    def __init__(self, start, change):
        """Tweenable:
            Holds values for anything that can be tweened
            these are normally only created by Tweens"""
        self.startValue = start
        self.change = change

if __name__=="__main__":
    class TweenTestObject:
        def __init__(self):
            self.pos = 20
            self.rot = 50

        def update(self):
            print(self.pos, self.rot)

        @property
        def pos(self):
            return self.__pos

        @pos.setter
        def pos(self, value):
            self.__pos = value

        def setRotation(self, rot):
            self.rot = rot

        def getRotation(self):
            return self.rot

        def complete(self):
            print("I'm done tweening now mommy!")

    class Sprite(object):
        def __init__(self):
            self.x = 0
            self.y = 0
            self.tweener = Tweener()
            self.mt = self.tweener.addTween(self, tweenTime=.1, tweenType=easing.linear.easeNone, x=100, y=999)

        @property
        def x(self):
            return self.__x

        @x.setter
        def x(self, value):
            self.__x = value

    def principal():
        import time
        o = Sprite()
        print(o.x, o.y)
        mt = o.mt
        s = time.clock()
        changed = False
        while o.tweener.hasTweens():
            tm = time.clock()
            d = tm-s
            s = tm
            o.tweener.update(d)
            if mt.delta > 1.0 and not changed:
                changed = True
        print(o.x, o.y)

    def main():
        import time
        T = Tweener()
        tst = TweenTestObject()
        mt = T.addTween(tst, setRotation=500.0, tweenTime=2.5, tweenType=easing.linear.easeNone,
                        pos=-200, tweenDelay=0.4, onCompleteFunction=tst.complete,
                        onUpdateFunction=tst.update)
        s = time.clock()
        changed = False
        while T.hasTweens():
            tm = time.clock()
            d = tm - s
            s = tm
            T.update(d)
            if mt.delta > 1.0 and not changed:

                tweenable = mt.getTweenable( "setRotation" )

                T.addTween(tweenable, change=-1000, tweenTime=0.7)
                T.addTween(mt, duration=-0.2, tweenTime=0.2)
                changed = True
            #print(mt.duration)
            print(tst.getRotation(), tst.pos)
            time.sleep(0.06)
        print(tst.getRotation(), tst.pos)

    main()
