import pygame
import time

from events import (
    CharactorMoveEvent,
    CharactorMoveRequest,
    CharactorPlaceEvent,
    TickEvent,
)
from patterns import AbsListener
from preferences import (
    DIRECTION_DOWN,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    DIRECTION_UP,
    FPS,
    MOVING_TIME_SECONDS as MTS,
    SIZE_TILE,
)
from utils import pytweener
from utils.imageutils import (
    SurfaceImage,
    Surfaces,
)

__all__ = (
    'CharactorSprite',
    'SectorSprite',
    'UmiSector',
)


class SectorSprite(pygame.sprite.DirtySprite):
    '''sprite of a void sector'''
    def __init__(self, sector, group=None, location=(0,0)):
        super(SectorSprite, self).__init__(group)
        grounds = SurfaceImage('Tileset- ground.png')
        default_grounds = Surfaces.listSurface(grounds, (13, 8))
        self.images = default_grounds
        self.image = Surfaces.scale(default_grounds[0], (SIZE_TILE, SIZE_TILE))
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.topleft = location
        self.sector = sector


class UmiSector(SectorSprite):
    def __init__(self, sector, group=None, location=(0,0)):
        super(UmiSector, self).__init__(sector, group, location)
        self.image = self.images[40]
        self.image = Surfaces.scale(self.image, (SIZE_TILE, SIZE_TILE))
        self.rect = self.image.get_rect()
        self.rect.topleft = location


class CharactorSprite(pygame.sprite.DirtySprite, AbsListener):
    '''sprite of the main character'''
    STAND = 1

    def __init__(self, ev_manager, charactor, group=None, location=(0,0)):
        super(CharactorSprite, self).__init__(group)

        self.ev_manager = ev_manager
        self.ev_manager.registerListener(self)

        self.__tweener = pytweener.Tweener()

        self.charactor = charactor

        aux = Surfaces.listSurface(SurfaceImage('walk_front2.png'), (3,1))
        self.images = {DIRECTION_DOWN : aux}
        aux = Surfaces.listSurface(SurfaceImage('walk_sleft2.png'), (3,1))
        self.images.update({DIRECTION_LEFT : aux})
        aux = Surfaces.listSurface(SurfaceImage('walk_sright2.png'), (3,1))
        self.images.update({DIRECTION_RIGHT : aux})
        aux = Surfaces.listSurface(SurfaceImage('walk_back2.png'), (3,1))
        self.images.update({DIRECTION_UP : aux})

        self.rect = aux[0].get_rect()
        self.rect.topleft = location
        
        self.last_direction = DIRECTION_DOWN
        self.image = self.images[self.last_direction][self.STAND]

        self.last_move = 1 # last move who took charactor
        self.is_moving = 0 # if is moving
        self.__time = 0 # to make transition of images when is moving
        self.__has_change = 0 # to change images when is moving in a time
        self.__delay = MTS*(1/2.) # delay to change a certain frame

    def move(self, direction):
        '''when a charactor starts to move'''
        self.is_moving = 1
        self.dirty = 1
        self.__time = time.time()
        y = self.rect.y
        x = self.rect.x
        if direction == DIRECTION_UP:
            y -= SIZE_TILE - 3
        elif direction == DIRECTION_DOWN:
            y += SIZE_TILE - 3
        elif direction == DIRECTION_LEFT:
            x -= SIZE_TILE - 3
        elif direction == DIRECTION_RIGHT:
            x += SIZE_TILE - 3
        tween_time = MTS+.01
        tween_type = pytweener.easing.linear.easeOut
        self.__tweener.addTween(self.rect,
                                x=x,
                                y=y,
                                tweenTime=tween_time,
                                tweenType=tween_type
                                )
        if direction == self.last_direction:
            if self.last_move == 2:
                self.image = self.images[self.last_direction][0]
                self.last_move = 0
            else:
                self.image = self.images[self.last_direction][2]
                self.last_move = 2
        else:
            self.image = self.images[direction][0]
            self.last_direction = direction
            self.last_move = 0

    def stand(self):
        '''when charactor was placed or is standing in a sector
        standing in a sector occurs when charactor finished a move'''
        self.dirty = 1
        self.image = self.images[self.last_direction][self.STAND]
        self.is_moving = 0
        self.__has_change = 0

    def facingTo(self, direction):
        '''change the facing view if charactor can't move'''
        if direction != self.last_direction:
            self.dirty = 1
            self.last_direction = direction
            self.image = self.images[self.last_direction][self.STAND]

    def __updateTweens(self):
        self.dirty = 1
        self.__tweener.update(FPS/1000.0)

    def notify(self, event):
        '''notifies this object about what method must has has execute'''
        # if not moving and system has asks to move
        if not self.is_moving and isinstance(event, CharactorMoveRequest):
            # if movement is possible
            if self.charactor.sector.movePossible(event.direction):
                self.move(event.direction)
            else:
                self.facingTo(event.direction)
        elif isinstance(event, CharactorPlaceEvent): # put charactor in map
            self.stand()
        elif isinstance(event, CharactorMoveEvent): # charactor has moved
            self.stand()
        elif isinstance(event, TickEvent):
            if self.is_moving: # if charactor is performing a movement
                if (time.time()-self.__time) > (self.__delay)\
                and self.__has_change == 0: # change images in a certain time while is moving
                    self.dirty = 1
                    self.__has_change = 1
                    self.image = self.images[self.last_direction][self.STAND]
                if self.__tweener.hasTweens():
                    self.__updateTweens()
