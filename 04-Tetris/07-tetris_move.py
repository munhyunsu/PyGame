import sys
from math import sqrt
import random

import pygame
from pygame.locals import QUIT, KEYDOWN, K_UP, K_LEFT, K_RIGHT, K_DOWN, K_SPACE, K_ESCAPE

from material import *


class Block:
    def __init__(self, name):
        self.turn = 0
        self.type = BLOCKS[name]
        self.data = self.type[self.turn]
        self.size = int(sqrt(len(self.data))) 
        self.xpos = (WIDTH - self.size)//2
        self.ypos = 0

    def draw(self):
        for index in range(len(self.data)):
            xpos = index % self.size
            ypos = index // self.size
            val = self.data[index]
            if ((0 <= ypos + self.ypos < HEIGHT) and
                (0 <= xpos + self.xpos < WIDTH) and 
                (val != 'B')):
                x_pos = 25 + (xpos + self.xpos) * 25
                y_pos = 25 + (ypos + self.ypos) * 25
                pygame.draw.rect(SURFACE, COLORS[val],
                                 (x_pos, y_pos, 24, 24))

    def left(self):
        self.xpos = self.xpos-1

    def right(self):
        self.xpos = self.xpos+1

    def down(self):
        self.ypos = self.ypos+1

    def up(self):
        self.turn = (self.turn+1)%4
        self.data = self.type[self.turn]


def get_block():
    name = random.choice(list(BLOCKS.keys()))
    block = Block(name)
    return block


# 전역 변수
pygame.init()
pygame.key.set_repeat(30, 30)
SURFACE = pygame.display.set_mode([600, 600])
FPSCLOCK = pygame.time.Clock()
WIDTH = 10 + 2
HEIGHT = 20 + 1
FIELD = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
BLOCK = None
FPS = 15


def main():
    global BLOCK
    score = 0
    if BLOCK is None:
        BLOCK = get_block()

    # 메시지
    smallfont = pygame.font.SysFont(None, 36)

    for ypos in range(HEIGHT):
        for xpos in range(WIDTH):
            FIELD[ypos][xpos] = 'W' if xpos == 0 or xpos == WIDTH - 1 else 'B'
    for index in range(WIDTH):
        FIELD[HEIGHT-1][index] = 'W'

    # 게임 무한 루프를 수행
    while True:
        # 이벤트 루프를 확인
        key = None
        for event in pygame.event.get():
            if event.type == QUIT: # 종료 이벤트
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                key = event.key
                if key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if key == K_UP:
            BLOCK.up()
        elif key == K_RIGHT:
            BLOCK.right()
        elif key == K_LEFT:
            BLOCK.left()
        elif key == K_DOWN:
            BLOCK.down()

        # Draw FIELD
        SURFACE.fill((0, 0, 0))
        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                value = FIELD[ypos][xpos]
                pygame.draw.rect(SURFACE, COLORS[value],
                                 (xpos*25 + 25, ypos*25 + 25, 24, 24))

        BLOCK.draw()

        # 점수 나타내기
        score_str = str(score).zfill(6)
        score_image = smallfont.render(score_str,
                                       True, (180, 180, 180))
        SURFACE.blit(score_image, (500, 30))

        # 언제나 그렇듯 화면을 업데이트
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()

