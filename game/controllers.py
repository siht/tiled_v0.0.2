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
)

__all__ = (
    'CPUSpinnerController',
    'KeyboardController',
    'KeyboardController2',
)


class DeadSpinnerException(Exception): pass


class CPUSpinnerController(AbsListener):
    '''sends ticks to the aplication
    based on script of sjbrown
    http://ezide.com/games/writing-games.html'''
    def __init__(self, ev_manager, fps=FPS):
        self.ev_manager = ev_manager
        self.ev_manager.registerListener(self)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.keep_going = 1

    def run(self):
        if not self.keep_going:
            raise DeadSpinnerException()
        while self.keep_going:
            aps = self.clock.tick(self.fps)
            ev = TickEvent(aps)
            self.ev_manager.post(ev)

    def notify(self, event: TypeEvent):
        if isinstance(event, QuitEvent):
            #this will stop the while loop from running
            self.keep_going = 0


class KeyboardController(AbsListener):
    '''...
    based on script of sjbrown
    http://ezide.com/games/writing-games.html'''
    def __init__(self, ev_manager: Mediator):
        self.ev_manager = ev_manager
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

    def notify(self, event: TypeEvent):
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
    MOVEMENT_KEYS = (K_UP, K_DOWN, K_RIGHT, K_LEFT)
    KEY_DIRECTIONS = {
        K_UP: DIRECTION_UP,
        K_DOWN: DIRECTION_DOWN,
        K_LEFT: DIRECTION_LEFT,
        K_RIGHT: DIRECTION_RIGHT,
    }

    def __init__(self, ev_manager: Mediator):
        self.ev_manager = ev_manager
        self.ev_manager.registerListener(self)
        self.movement_keys_pressed = []

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

    def _get_last_movement_key_pressed(self):
        return self.movement_keys_pressed[0]

    def _get_direction_movement(self, key: int) -> int:
        return self.KEY_DIRECTIONS.get(key, None)

    def notify(self, event: TypeEvent):
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
