from typing import (
    Dict,
    List,
    Tuple,
    Union,
)

import pygame
from pygame.event import Event as PygameEvent
from pygame.locals import (
    K_DOWN,
    K_ESCAPE,
    K_LEFT,
    K_RETURN,
    K_RIGHT,
    K_UP,
    KEYDOWN,
    KEYUP,
    QUIT,
)
from twisted.internet.main import installReactor
from twisted.internet.selectreactor import SelectReactor
from twisted.spread import pb

from events import (
    CharactorMoveRequest,
    GameStartRequest,
    QuitEvent,
    TickEvent,
    TypeEvent,
)
from patterns import (
    AbsListener,
    Mediator,
)
from preferences import (
    DIRECTION_DOWN,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    DIRECTION_UP,
    FPS,
    PORT,
)
import pygame_test

__all__ = (
    'CPUSpinnerController',
    'KeyboardController',
    'KeyboardController2',
    'NetworkClientController',
)


class DeadSpinnerException(Exception): pass


class CPUSpinnerController(AbsListener):
    '''sends ticks to the aplication
    based on script of sjbrown
    http://ezide.com/games/writing-games.html'''
    def __init__(self, ev_manager: Mediator, fps: int=FPS) -> None:
        self.ev_manager: Mediator = ev_manager
        self.ev_manager.registerListener(self)
        self.clock = pygame.time.Clock()
        self.fps: int = fps
        self.keep_going: int = 1

    def run(self) -> None:
        if not self.keep_going:
            raise DeadSpinnerException()
        while self.keep_going:
            aps = self.clock.tick(self.fps)
            ev = TickEvent(aps)
            self.ev_manager.post(ev)

    def notify(self, event: TypeEvent) -> None:
        if isinstance(event, QuitEvent):
            #this will stop the while loop from running
            self.keep_going = 0


class KeyboardController(AbsListener):
    '''...
    based on script of sjbrown
    http://ezide.com/games/writing-games.html'''
    def __init__(self, ev_manager: Mediator) -> None:
        self.ev_manager: Mediator = ev_manager
        self.ev_manager.registerListener(self)

    def _somebody_close_window(self, event: PygameEvent) -> bool:
        return event.type == QUIT

    def _escape_was_pressed(self, event: PygameEvent) -> bool:
        return event.type == KEYDOWN and event.key == K_ESCAPE

    def _up_arrow_was_pressed(self, event: PygameEvent) -> bool:
        return event.type == KEYDOWN and event.key == K_UP

    def _down_arrow_was_pressed(self, event: PygameEvent) -> bool:
        return event.type == KEYDOWN and event.key == K_DOWN

    def _left_arrow_was_pressed(self, event: PygameEvent) -> bool:
        return event.type == KEYDOWN and event.key == K_LEFT

    def _right_arrow_was_pressed(self, event: PygameEvent) -> bool:
        return event.type == KEYDOWN and event.key == K_RIGHT

    def _enter_was_pressed(self, event: PygameEvent) -> bool:
        return event.type == KEYDOWN and event.key == K_RETURN

    def notify(self, event: TypeEvent) -> None:
        if isinstance(event, TickEvent):
            #Handle Input Events
            for pygame_event in pygame.event.get():
                ev = None
                if self._somebody_close_window(pygame_event):
                    ev = QuitEvent()
                elif self._escape_was_pressed(pygame_event):
                    ev = QuitEvent()
                elif self._up_arrow_was_pressed(pygame_event):
                    direction = DIRECTION_UP
                    ev = CharactorMoveRequest(direction)
                elif self._down_arrow_was_pressed(pygame_event):
                    direction = DIRECTION_DOWN
                    ev = CharactorMoveRequest(direction)
                elif self._left_arrow_was_pressed(pygame_event):
                    direction = DIRECTION_LEFT
                    ev = CharactorMoveRequest(direction)
                elif self._right_arrow_was_pressed(pygame_event):
                    direction = DIRECTION_RIGHT
                    ev = CharactorMoveRequest(direction)
                elif self._enter_was_pressed(pygame_event):
                    ev = GameStartRequest()
                if ev:
                    self.ev_manager.post(ev)


class KeyboardController2(AbsListener):
    '''this controller allows to send multiple movement events until keys isnt pressed'''
    MOVEMENT_KEYS: Tuple[int] = (K_UP, K_DOWN, K_RIGHT, K_LEFT)
    KEY_DIRECTIONS: Dict[int, int] = {
        K_UP: DIRECTION_UP,
        K_DOWN: DIRECTION_DOWN,
        K_LEFT: DIRECTION_LEFT,
        K_RIGHT: DIRECTION_RIGHT,
    }

    def __init__(self, ev_manager: Mediator) -> None:
        self.ev_manager: Mediator = ev_manager
        self.ev_manager.registerListener(self)
        self.movement_keys_pressed: List[int] = []

    def _somebody_close_window(self, event: PygameEvent) -> bool:
        return event.type == QUIT

    def _keyboard_is_pressed(self, event: PygameEvent) -> bool:
        return event.type == KEYDOWN

    def _escape_was_pressed(self, event: PygameEvent) -> bool:
        return self._keyboard_is_pressed(event) and event.key == K_ESCAPE

    def _enter_was_pressed(self, event: PygameEvent) -> bool:
        return event.type == KEYDOWN and event.key == K_RETURN

    def _movement_keys_was_pressed(self, event: PygameEvent) -> bool:
        return event.key in self.MOVEMENT_KEYS and event.key not in self.movement_keys_pressed

    def _some_key_was_stopped_pressing(self, event: PygameEvent) -> bool:
        return event.type == KEYUP

    def _movement_keys_still_pressed(self, event: PygameEvent) -> bool:
        return event.key in self.MOVEMENT_KEYS

    def _update_keys_pressed(self, event: PygameEvent) -> None:
        if self._keyboard_is_pressed(event):
            if self._movement_keys_was_pressed(event):
                self.movement_keys_pressed.insert(0, event.key) # agregar al principio para saber la última presionada
        elif self._some_key_was_stopped_pressing(event):
            if self._movement_keys_still_pressed(event):
                index = self.movement_keys_pressed.index(event.key)
                del(self.movement_keys_pressed[index])

    def _get_last_movement_key_pressed(self) -> int:
        return self.movement_keys_pressed[0]

    def _get_direction_movement(self, key: int) -> Union[int, None]:
        return self.KEY_DIRECTIONS.get(key, None)

    def notify(self, event: TypeEvent) -> None:
        if isinstance(event, TickEvent):
            ev = None
            for pygame_event in pygame.event.get():
                if self._somebody_close_window(pygame_event):
                    ev = QuitEvent()
                elif self._escape_was_pressed(pygame_event):
                    ev = QuitEvent()
                elif self._enter_was_pressed(pygame_event):
                    ev = GameStartRequest()
                ########################################################
                self._update_keys_pressed(pygame_event)
                ########################################################
            if not ev and self.movement_keys_pressed:
                last_key_pressed = self._get_last_movement_key_pressed()
                direction = self._get_direction_movement(last_key_pressed)
                ev = CharactorMoveRequest(direction)
            if ev:
                self.ev_manager.post(ev)


class NetworkClientController(AbsListener, pb.Root):
    '''...'''
    def __init__(self, ev_manager: Mediator) -> None:
        self.ev_manager: Mediator = ev_manager
        self.ev_manager.registerListener(self)

    def remote_GameStartRequest(self) -> int:
        ev = GameStartRequest()
        self.ev_manager.post(ev)
        return 1

    def remote_CharactorMoveRequest(self, direction: int) -> int:
        ev = CharactorMoveRequest(direction)
        self.ev_manager.post(ev)
        return 1

    def notify(self, event: TypeEvent) -> None:
        '''implementation no needed'''
        pass


class ReactorController(SelectReactor):
    def __init__(self):
        super().__init__()
        connection = self.connectTCP('localhost', PORT, factory)
        pygame_test.prepare()
        installReactor(self)

    def doIteration(self, delay):
        print('calling doIteration')
        super().doIteration(delay)
        retval = pygame_test.iterate()
        if retval == False:
            thing_in_control.stop()


class ReactorSlaveController:
    def __init__(self):
        self.keep_going = True
        self.reactor = SelectReactor()
        installReactor(self.reactor)
        global factory
        connection = self.reactor.connectTCP('localhost', PORT, factory)
        self.reactor.startRunning()
        self.future_call = None
        self.future_call_timeout = None
        pygame_test.prepare()

    def iterate(self):
        print('in iterate')
        self.reactor.runUntilCurrent()
        self.reactor.doIteration(0)
        #t2 = self.reactor.timeout()
        #print 'timeout', t2
        #t = self.reactor.running and t2
        #self.reactor.doIteration(t)

    def run(self):
        clock = pygame.time.Clock()

        def stupid_test():
            print('stupid test!')

        self.reactor.callLater(2, stupid_test)
        while self.keep_going:
            time_change = clock.tick(FPS)
            if self.future_call:
                self.future_call_timeout -= time_change
                print(f'future call in {self.future_call_timeout}')
                if self.future_call_timeout <= 0:
                    self.future_call()
                    self.future_call_timeout = None
                    self.future_call= None
            retval = pygame_test.iterate()
            if retval == False:
                thing_in_control.stop()
            self.iterate()

    def stop(self):
        print('stopping')
        self.reactor.stop()
        self.keep_going = False

    def callLater(self, when, fn):
        self.future_call_timeout = when*1000
        self.future_call = fn
        print(f'future call in {self.future_call_timeout}')


class LoopingCallController:
    def __init__(self):
        from twisted.internet import reactor
        from twisted.internet.task import LoopingCall
        self.reactor = reactor
        connection = self.reactor.connectTCP('localhost', PORT, factory)
        self.looping_call = LoopingCall(self.iterate)
        pygame_test.prepare()

    def iterate(self):
        print('looping call controller in iterate')
        retval = pygame_test.iterate()
        if retval == False:
            thing_in_control.stop()

    def run(self):
        interval = 1.0 / FPS
        self.looping_call.start(interval)
        self.reactor.run()

    def stop(self):
        self.reactor.stop()

    def callLater(self, when, fn):
        self.reactor.callLater(when, fn)


if __name__ == '__main__':
    '''first activate server'''

    global server
    server = None

    def got_server(serv):
        print('-'*79)
        print(f'got server {serv}')
        global server
        server = serv
        # stop in exactly 5 seconds
        thing_in_control.callLater(5.0, stop_loop)


    def stop_loop():
        print('-'*79)
        print('stopping the loop')
        thing_in_control.stop()

    factory = pb.PBClientFactory()
    d = factory.getRootObject()
    d.addCallback(got_server)


    import sys
    if len(sys.argv) < 2:
        print('usage: controllers.py 1|2|3')
        sys.exit(1)
    elif sys.argv[1] == '1':
        thing_in_control = ReactorController()
    elif sys.argv[1] == '2':
        thing_in_control = ReactorSlaveController()
    else:
        thing_in_control = LoopingCallController()

    thing_in_control.run()

    print(server)
    print('end')

