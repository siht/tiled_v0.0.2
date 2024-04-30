'''
classes for some design patterns that are implemented
like plugins or are easy to implement
'''
from __future__ import annotations
from abc import (
    ABCMeta,
    abstractmethod,
)
from typing import List
from weakref import WeakKeyDictionary

from events import (
    TickEvent,
    TypeEvent,
    Type,
)


__all__ = (
    'AbsListener',
    'FlyWeight',
    'Mediator',
    'Singleton',
    'TypeListener',
)


class Mediator:
    '''
    Event Manager copied of Sjbrown
    this object is responsible for coordinating most communication
    between the Model, View, and Controller.
    The heart of MVC
    http://ezide.com/games/writing-games.html'''
    def __init__(self):
        self.listeners: WeakKeyDictionary[TypeListener, int] = WeakKeyDictionary()
        self.event_queue: List[TypeEvent] = []

    def debug(self, ev: TypeEvent):
        print(f"   Message: {ev.name}")

    def registerListener(self, listener: TypeListener):
        #if not hasattr(listener, "Notify"): raise blah blah...
        self.listeners[listener] = 1

    def unregisterListener(self, listener: TypeListener):
        if listener in self.listeners.keys():
            del self.listeners[listener]

    def post(self, event: TypeEvent):
        if not isinstance(event, TickEvent): 
            self.event_queue.append(event)
        else:
            events = self.event_queue[:]
            self.event_queue = []
            while len(events) > 0:
                ev = events.pop(0)
                self.debug(ev)
                for listener in list(self.listeners):
                    listener.notify(ev)
            #at the end, notify listeners of the Tick event
            for listener in list(self.listeners):
                listener.notify(event)


class AbsListener(metaclass=ABCMeta):
    '''Listener for Mediator
    usage:
    
    class Other(AbsListener):
        # override the abstract methods
        ...
    '''

    @abstractmethod
    def notify(self, ev: TypeEvent):
        pass


TypeListener = Type[AbsListener]


class FlyWeight(type):
    '''
    copied of david villa
    http://crysol.org/es/user/3
    pattern flyweight as metaclass (level: aplication)
    add this metaclass in the definition of the class
    i.e.
    class A(object):
        __metaclass__ = FlyWeight
        ...
    '''
    def __init__(cls, name, bases, dct):
        cls.__instances = {}
        type.__init__(cls, name, bases, dct)
 
    def __call__(cls, key, *args, **kw):
        instance = cls.__instances.get(key)
        if instance is None:
            instance = type.__call__(cls, key, *args, **kw)
            cls.__instances[key] = instance
        return instance


class Singleton(type):
    '''
    copied of david villa
    http://crysol.org/es/user/3
    pattern singleton as metaclass (level: aplication)
    add this metaclass in the definition of the class
    i.e.
    class A(object):
        __metaclass__ = Singleton
        ...
    '''
    def __init__(cls, name, bases, dct):
        cls.__instance = None
        type.__init__(cls, name, bases, dct)
 
    def __call__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args,**kw)
        return cls.__instance
