import sys

import pygame
from pygame.locals import QUIT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.display.set_caption('PyGame Window') # PyGame Window Title

SURFACE = pygame.display.set_mode((400, 300)) # PyGame Window Size (x, y)


def main():
    sysfont = pygame.font.SysFont(None, 36) # Load system font
    counter = 0

    while True:
        SURFACE.fill(WHITE)

        for event in pygame.event.get(): # Get events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        counter = counter + 1
        count_text = sysfont.render(f'count is {counter}', 
                                    True,
                                    GREY)
        SURFACE.blit(count_text, (50, 50))

        pygame.display.update()


if __name__ == '__main__':
    main()

