# basic settings
from typing import Tuple

WINDOW_SIZE: Tuple[int, int] = (800, 600)
SIZE_TILE: int = 72
SECTOR_HEIGHT: int = 7
SECTOR_WIDTH: int = 7
# some colors
RED: Tuple[int, int, int, int] = (255, 0, 0, 0)
GREEN: Tuple[int, int, int, int] = (0, 255, 0, 0)
BLUE: Tuple[int, int, int, int] = (0, 0, 255, 0)
BLACK: Tuple[int, int, int, int] = (0, 0, 0, 0)
WHITE: Tuple[int, int, int, int] = (255, 255, 255, 0)
# common directions
DIRECTION_UP: int = 0
DIRECTION_DOWN: int = 1
DIRECTION_LEFT: int = 2
DIRECTION_RIGHT: int = 3
# time to pass to one sector to another
MOVING_TIME_SECONDS: float = .3
# frames per second
FPS: int = 30
PORT: int = 8080
