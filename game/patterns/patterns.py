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

def debug(msg):
	print(msg)


__all__ = (
    'AbsListener',
    'FlyWeight',
    'Mediator',
    'NoTickMediator',
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
    def __init__(self) -> None:
        self.listeners: WeakKeyDictionary[TypeListener, int] = WeakKeyDictionary()
        self.event_queue: List[TypeEvent] = []
        self.listeners_to_add: List[TypeListener] = []
        self.listeners_to_remove: List[TypeListener] = []

    def registerListener(self, listener: TypeListener) -> None:
        self.listeners_to_add.append(listener)

    def actuallyUpdateListeners(self) -> None:
        for listener in self.listeners_to_add:
            self.listeners[listener] = 1
        for listener in self.listeners_to_remove:
            if listener in self.listeners:
                del self.listeners[listener]

    def unregisterListener(self, listener: TypeListener) -> None:
        self.listeners_to_remove.append(listener)

    def post(self, event: TypeEvent) -> None:
        if not isinstance(event, TickEvent):
            debug(f'     Message:  {event.name}')
        self.event_queue.append(event)
        if isinstance(event, TickEvent):
            # Consume the event queue every Tick.
            self.actuallyUpdateListeners()
            self.consumeEventQueue()

    def consumeEventQueue(self) -> None:
        i = 0
        while i < len(self.event_queue):
            event = self.event_queue[i]
            for listener in self.listeners:
                # Note: a side effect of notifying the listener
                # could be that more events are put on the queue
                # or listeners could Register / Unregister
                listener.notify(event)
            i += 1
            if self.listeners_to_add:
                self.actuallyUpdateListeners()
        #all code paths that could possibly add more events to 
        # the eventQueue have been exhausted at this point, so 
        # it's safe to empty the queue
        self.event_queue = []


class NoTickMediator(Mediator):
    def __init__(self) -> None:
        super().__init__()
        self._lock = False

    def post(self, event: TypeEvent) -> None:
        super().post(event)
        if not self._lock:
            self._lock = True
            self.actuallyUpdateListeners()
            self.consumeEventQueue()
            self._lock = False


class AbsListener(metaclass=ABCMeta):
    '''Listener for Mediator
    usage:
    
    class Other(AbsListener):
        # override the abstract methods
        ...
    '''

    @abstractmethod
    def notify(self, ev: TypeEvent) -> None:
        pass


TypeListener = Type[AbsListener]


class FlyWeight(type):
    '''
    copied of david villa
    http://crysol.org/es/user/3
    pattern flyweight as metaclass (level: aplication)
    add this metaclass in the definition of the class
    i.e.
    class A(metaclass=FlyWeight):
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
    class A(metaclass=Singleton):
        ...
    '''
    def __init__(cls, name, bases, dct):
        cls.__instance = None
        type.__init__(cls, name, bases, dct)
 
    def __call__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args,**kw)
        return cls.__instance
