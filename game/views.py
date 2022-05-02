'''most of this script is based on scripts of sjbrown
http://ezide.com/games/writing-games.html'''

import pygame

from events import (
    TickEvent,
    MapBuiltEvent,
    CharactorMoveEvent,
    CharactorPlaceEvent,
)
from graphics import (
    SectorSprite,
    CharactorSprite,
    UmiSector
)
from patterns import AbsListener
import preferences as pref

__all__ = (
    'MainView',
)

class MainView(AbsListener):
    def __init__(self, ev_manager):
        self.ev_manager = ev_manager
        self.ev_manager.registerListener(self)
        pygame.init()
        self.window = pygame.display.set_mode(pref.WINDOW_SIZE)
        pygame.display.set_caption('my first game mvc')
        self.background = pygame.Surface(self.window.get_size())
        self.background.fill(pref.BLACK)
        self.back_sprites = pygame.sprite.LayeredDirty()
        pygame.display.flip()
        self.front_sprites = pygame.sprite.LayeredDirty()
        self.dirty_rects = None

    def showMap(self, game_map): # improve this method
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()
        size = pref.SIZE_TILE
        position_rect = pygame.Rect((0, size, size, size))

        i = 0
        for sector in game_map.sectors:
            if i < pref.SECTOR_WIDTH:
                position_rect = position_rect.move(size,0)
            else:
                i = 0
                position_rect = position_rect.move(-(size*(pref.SECTOR_WIDTH-1)), size)
            i += 1
            new_sprite = UmiSector(sector, self.back_sprites)
            new_sprite.rect = position_rect
            self.background.blit(new_sprite.image, new_sprite.rect)
            new_sprite = None

    def getCharactorSprite(self, charactor):
        #there will be only one
        for s in self.front_sprites:
            return s
        return None

    def getSectorSprite(self, sector):
        for s in self.back_sprites:
            if hasattr(s, "sector") and s.sector == sector:
                return s

    def putCharactor(self, charactor):
        sector = charactor.sector
        charactor_sprite = CharactorSprite(self.ev_manager, charactor, self.front_sprites)
        sector_sprite = self.getSectorSprite(sector)
        charactor_sprite.rect.midbottom = sector_sprite.rect.midbottom

    def showCharactor(self, charactor):
        sector = charactor.sector
        charactor_sprite = self.getCharactorSprite(charactor)
        sector_sprite = self.getSectorSprite(sector)
        charactor_sprite.rect.midbottom = sector_sprite.rect.midbottom

    def draw(self):
        # self.back_sprites.clear(self.window, self.background)
        self.front_sprites.clear(self.window, self.background)

        dirty_rects1 = self.back_sprites.draw(self.window)
        dirty_rects2 = self.front_sprites.draw(self.window)
        self.dirty_rects = dirty_rects1 + dirty_rects2

    def notify(self, event):
        if isinstance(event, TickEvent):
            self.draw()
            if self.dirty_rects:
                pygame.display.update(self.dirty_rects)
                self.dirty_rects = []
        elif isinstance(event, MapBuiltEvent):
            game_map = event.map
            self.showMap(game_map)
        elif isinstance(event, CharactorPlaceEvent):
            self.putCharactor(event.charactor)
        elif isinstance(event, CharactorMoveEvent):
            self.showCharactor(event.charactor)
