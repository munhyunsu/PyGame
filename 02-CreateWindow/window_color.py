import sys

import pygame
from pygame.locals import QUIT

pygame.init()
pygame.display.set_caption('PyGame Window') # PyGame Window Title

SURFACE = pygame.display.set_mode((400, 300)) # PyGame Window Size (x, y)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def main():
    while True:
        SURFACE.fill(BLACK) # White

        for event in pygame.event.get(): # Get events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
        pygame.display.update()


if __name__ == '__main__':
    main()

