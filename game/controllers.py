from __future__ import print_function
from events import TickEvent, GameStartRequest, CharactorMoveRequest, QuitEvent
from patterns import AbsListener
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_RETURN
import pygame
from preferences import DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT, FPS

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
            raise Exception('dead spinner')
        while self.keep_going:
            aps = self.clock.tick(self.fps)
            ev = TickEvent(aps)
            self.ev_manager.post(ev)

    def notify(self, event):
        if isinstance(event, QuitEvent):
            #this will stop the while loop from running
            self.keep_going = 0

class KeyboardController(AbsListener):
    '''...
    based on script of sjbrown
    http://ezide.com/games/writing-games.html'''
    def __init__(self, ev_manager):
        self.ev_manager = ev_manager
        self.ev_manager.registerListener(self)

    def notify(self, event):
        if isinstance(event, TickEvent):
            #Handle Input Events
            for event in pygame.event.get():
                ev = None
                if event.type == QUIT:
                    ev = QuitEvent()
                elif event.type == KEYDOWN \
                    and event.key == K_ESCAPE:
                    ev = QuitEvent()
                elif event.type == KEYDOWN \
                    and event.key == K_UP:
                    direction = DIRECTION_UP
                    ev = CharactorMoveRequest(direction)
                elif event.type == KEYDOWN \
                    and event.key == K_DOWN:
                    direction = DIRECTION_DOWN
                    ev = CharactorMoveRequest(direction)
                elif event.type == KEYDOWN \
                    and event.key == K_LEFT:
                    direction = DIRECTION_LEFT
                    ev = CharactorMoveRequest(direction)
                elif event.type == KEYDOWN \
                    and event.key == K_RIGHT:
                    direction = DIRECTION_RIGHT
                    ev = CharactorMoveRequest(direction)
                elif event.type == KEYDOWN \
                    and event.key == K_RETURN:
                    ev = GameStartRequest()
                if ev:
                    self.ev_manager.post(ev)

class KeyboardController2(AbsListener):
    '''my own controller'''
    def __init__(self, ev_manager):
        self.ev_manager = ev_manager
        self.ev_manager.registerListener(self)

        # self.any_key_down = False
        self.keys_pressed = []
        self.available_keys = (K_UP, K_DOWN, K_RIGHT, K_LEFT)

    def notify(self, event):
        if isinstance(event, TickEvent):
            ev = None
            for event in pygame.event.get(): #va de cajon
                if event.type == QUIT:
                    ev = QuitEvent()
                elif event.type == KEYDOWN \
                    and event.key == K_ESCAPE:
                    ev = QuitEvent()
                elif event.type == KEYDOWN \
                    and event.key == K_RETURN:
                    ev = GameStartRequest()
                ########################################################
                if event.type == KEYDOWN:
                    if event.key in self.available_keys \
                      and event.key not in self.keys_pressed:
                        self.keys_pressed.insert(0, event.key)
                elif event.type == KEYUP:
                    if event.key in self.available_keys:
                        index = self.keys_pressed.index(event.key)
                        del(self.keys_pressed[index])
                ########################################################
            if not ev and self.keys_pressed:
                key = self.keys_pressed[0]
                direction = None
                if key == K_UP:
                    direction = DIRECTION_UP
                elif key == K_DOWN:
                    direction = DIRECTION_DOWN
                elif key == K_LEFT:
                    direction = DIRECTION_LEFT
                elif key == K_RIGHT:
                    direction = DIRECTION_RIGHT
                ev = CharactorMoveRequest(direction)
            if ev:
                self.ev_manager.post(ev)
