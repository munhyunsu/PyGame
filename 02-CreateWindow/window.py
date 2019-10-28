import sys

import pygame
from pygame.locals import QUIT

pygame.init()
pygame.display.set_caption('PyGame Window') # PyGame Window Title

SURFACE = pygame.display.set_mode((400, 300)) # PyGame Window Size (x, y)


def main():
    while True:
        SURFACE.fill((255, 255, 255)) # White

        for event in pygame.event.get(): # Get events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
        pygame.display.update()


if __name__ == '__main__':
    main()

