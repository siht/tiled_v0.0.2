'''models of the game
based on script of sjbrown
http://ezide.com/games/writing-games.html'''
import time

from events import (
    CharactorMoveEvent,
    CharactorMoveRequest,
    CharactorPlaceEvent,
    CharactorPlaceRequest,
    GameStartRequest,
    GameStartedEvent,
    MapBuiltEvent,
    TickEvent,
)
from patterns import AbsListener
from preferences import (
    DIRECTION_DOWN,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    DIRECTION_UP,
    MOVING_TIME_SECONDS,
    SECTOR_HEIGHT,
    SECTOR_WIDTH,
)

__all__ = (
    'Game',
    'Player',
    'Charactor',
    'Hero',
    'Map',
    'Sector',
)


class Game(AbsListener):
    STATE_PREPARING = 0
    STATE_RUNNING = 1
    STATE_PAUSED = 2

    state = STATE_PREPARING
    ev_manager = None
    players = []
    max_players = 1
    map = None

    def __init__(self, ev_manager):
        self.ev_manager = ev_manager
        self.ev_manager.registerListener(self)
        self.reset(ev_manager)

    def reset(self, ev_manager):
        self.state = self.STATE_PREPARING
        self.players = [Player(ev_manager)]
        self.max_players = 1
        self.map = Map(self.ev_manager)

    def start(self):
        self.map.build()
        self.state = self.STATE_RUNNING
        ev = GameStartedEvent(self)
        self.ev_manager.post(ev)

    def notify(self, event):
        if isinstance(event, GameStartRequest):
            if self.state == self.STATE_PREPARING:
                self.start()


class Player(AbsListener):
    """..."""
    ev_manager = None
    game = None
    charactors = None
    placeable_charactor_classes = None
    
    def __init__(self, ev_manager):
        self.ev_manager = ev_manager
        self.ev_manager.registerListener(self)
        self.game = None

        self.charactors = [Charactor(ev_manager)]

        self.placeable_charactor_classes = [Charactor]

    def getPlaceData(self):
        charactor = self.charactors[0]
        map = self.game.map
        sector =  map.sectors[map.sector_spawn]
        return [charactor, sector]

    def getMoveData(self):
        return [self.charactors[0]]

    def getGame(self, game):
        self.game = game

    def getData(self, playerDict):
        self.name = playerDict['name']

    def notify(self, event):
        pass


class Charactor(AbsListener):
    """..."""
    STATE_INACTIVE = 0
    STATE_ACTIVE = 1

    ev_manager = None
    sector = None
    state = STATE_INACTIVE
    is_moving = 0

    def __init__(self, ev_manager):
        self.ev_manager = ev_manager
        self.move_time = MOVING_TIME_SECONDS
        self.ev_manager.registerListener( self )
        self.is_moving = 0
        self.sector = None
        self.state = Charactor.STATE_INACTIVE

    def move(self, direction):
        if self.state == Charactor.STATE_INACTIVE:
            return

        if self.sector.movePossible(direction):
            new_sector = self.sector.neighbors[direction]
            self.__new_sector = new_sector
            self.__initial_time = time.time()
            self.is_moving = 1

    def moving(self):
        if (time.time() - self.__initial_time) >= self.move_time:
            ev = CharactorMoveEvent(self)
            self.is_moving = 0
            self.sector = self.__new_sector
            self.ev_manager.post(ev)

    def place(self, sector):
        self.sector = sector
        self.state = Charactor.STATE_ACTIVE

        ev = CharactorPlaceEvent(self)
        self.ev_manager.post(ev)

    def notify(self, event):
        if isinstance(event, CharactorPlaceRequest):
            self.place(event.sector)
        elif isinstance(event, CharactorMoveRequest) and not self.is_moving:
            self.move(event.direction)
        elif isinstance(event, GameStartedEvent):
            game_map = event.game.map
            self.place(game_map.sectors[game_map.sector_spawn])
        elif self.is_moving and isinstance(event, TickEvent):
            self.moving()


class Hero(Charactor): pass


class Map(AbsListener):
    """..."""
    STATE_PREPARING = 0
    STATE_BUILT = 1
    
    ev_manager = None
    state = STATE_PREPARING
    sectors = []
    sector_spawn = 0

    def __init__(self, ev_manager):
        self.ev_manager = ev_manager
        self.ev_manager.registerListener(self)
        self.state = self.STATE_PREPARING
        self.sectors = []
        self.sector_spawn = 0

    def build(self):
        # TO DO:
        # to think in any form to load a map
        # temp
        number_sector = list(range(SECTOR_HEIGHT*SECTOR_WIDTH))
        lenght_aux = len(number_sector)
        for i in number_sector:
            self.sectors.append(Sector(self.ev_manager))
        for i in number_sector:
            if not i < SECTOR_WIDTH:
                self.sectors[i].neighbors[DIRECTION_UP] = self.sectors[i - SECTOR_WIDTH]
            if i % SECTOR_WIDTH:
                self.sectors[i].neighbors[DIRECTION_LEFT] = self.sectors[i - 1]
            if not ((i % SECTOR_WIDTH) == (SECTOR_WIDTH-1)):
                self.sectors[i].neighbors[DIRECTION_RIGHT] = self.sectors[i + 1]
            if not ((lenght_aux - i - 1) < SECTOR_WIDTH):
                self.sectors[i].neighbors[DIRECTION_DOWN] = self.sectors[i + SECTOR_WIDTH]
        self.state = self.STATE_BUILT
        ev = MapBuiltEvent(self)
        self.ev_manager.post(ev)

    def notify(self, event):
        if isinstance(event, CharactorPlaceEvent):
            sect = event.charactor.sector
            self.sector_spawn = self.sectors.index(sect)+1


class Sector(object):
    '''map sectors, or tiles, no properties'''
    ev_manager = None
    neighbors = None
    
    def __init__(self, ev_manager):
        self.ev_manager = ev_manager
        self.neighbors = list(range(4))
        self.neighbors[DIRECTION_UP] = None
        self.neighbors[DIRECTION_DOWN] = None
        self.neighbors[DIRECTION_LEFT] = None
        self.neighbors[DIRECTION_RIGHT] = None

    def movePossible(self, direction):
        if self.neighbors[direction]:
            return 1
