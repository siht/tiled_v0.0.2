'''
An example of using the collision_resolver module

Pops up a window populated by randomly placed little squares.
You control the big square with the direction keys.
'''

from random import randint
import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


from preferences import (
    WINDOW_SIZE,
    GREEN,
)


RESOLUTION = WINDOW_SIZE
green = GREEN
avatar = None
avatarGroup = None
sceen = None
background = None
origBackground = None
screen = None

def main():
    clock = pygame.time.Clock()

    prepare()
    while True:
        clock.tick(2)
        retval = iterate()
        if not retval:
            return

def prepare():
    global screen
    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION)
    start()

def iterate():
    avatar.moveState[0] = randint(-9, 9)
    avatar.moveState[1] = randint(-9, 9)

    for ev in pygame.event.get():
        if ev.type == QUIT:
            return False
        if ev.type == KEYDOWN and ev.key == K_ESCAPE:
            return False

    #clear
    avatarGroup.clear(screen, background)

    #update
    avatarGroup.update()

    #draw
    avatarGroup.draw(screen)
    pygame.display.update()

    return True

def start():
    global avatar, avatarGroup, background, origBackground, screen
    background = pygame.Surface(RESOLUTION)
    off_black = (40, 10, 0)
    background.fill(off_black)

    # avatar will be a green square in the center of the screen
    avatar = Avatar()

    fixed_background_sprites = pygame.sprite.Group()
    for block in generate_random_blocks(30, RESOLUTION):
        if not block.rect.colliderect(avatar.rect):
            fixed_background_sprites.add(block)
    fixed_background_sprites.draw(background)

    avatar.collidables = fixed_background_sprites

    avatarGroup = pygame.sprite.Group()
    avatarGroup.add(avatar)

    screen.blit(background, (0, 0))
    pygame.display.flip()
    origBackground = background.copy()


class Avatar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 100))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.center = (RESOLUTION[0]/2, RESOLUTION[1]/2)
        self.moveState = [0, 0]
        self.collidables = None

    def update(self):
        if self.moveState[0] or self.moveState[1]:
            screen = pygame.display.get_surface()
            screen.blit( origBackground, (0, 0))
        self.rect.move_ip(*self.moveState)
        
class SimpleSprite(pygame.sprite.Sprite):
    def __init__(self, surface):
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = self.image.get_rect()

def generate_random_blocks(how_many, position_bounds):
    lower_color_bound = (100, 100, 100)
    upper_color_bound = (200, 200, 200)

    lower_x_bound, lower_y_bound = (0, 0)
    upper_x_bound, upper_y_bound = position_bounds

    lower_width_bound, lower_height_bound = (30, 30)
    upper_width_bound, upper_height_bound = (60, 60)

    for i in range(how_many):
        color = [
            randint(lower_color_bound[i], upper_color_bound[i]) for i in range(3)
        ]
        pos = [
            randint(lower_x_bound, upper_x_bound), randint(lower_y_bound,upper_y_bound)
        ]
        size = [
            randint(lower_width_bound, upper_width_bound), randint(lower_height_bound, upper_height_bound)
        ]

        s = SimpleSprite(pygame.Surface(size))
        s.image.fill(color)
        s.rect.topleft = pos
        yield s


if __name__ == '__main__':
    main()

