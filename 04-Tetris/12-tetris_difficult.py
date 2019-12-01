import sys
from math import sqrt, ceil
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
        self.stop = 0

    def update(self):
        global BLOCK
        erased = 0
        if is_overlapped(self.xpos, self.ypos+1, self.turn):
            for y_offset in range(self.size):
                for x_offset in range(self.size):
                    if ((0 <= self.xpos+x_offset < WIDTH) and
                        (0 <= self.ypos+y_offset < HEIGHT)):
                        val = self.data[y_offset*self.size \
                                            + x_offset]
                        if val != 'B':
                            FIELD[self.ypos+y_offset]\
                                 [self.xpos+x_offset] = val
            BLOCK = get_block()
            erased = erase_line()
        else:
            self.stop = self.stop + 1
            if self.stop > FPS/DIFFICULT:
                self.stop = 0
                self.ypos = self.ypos + 1
        return erased

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
        if not is_overlapped(self.xpos-1, self.ypos, self.turn):
            self.xpos = self.xpos-1

    def right(self):
        if not is_overlapped(self.xpos+1, self.ypos, self.turn):
            self.xpos = self.xpos+1

    def down(self):
        if not is_overlapped(self.xpos, self.ypos+1, self.turn):
            self.ypos = self.ypos+1

    def up(self):
        if not is_overlapped(self.xpos, self.ypos, (self.turn+1)%4):
            self.turn = (self.turn+1)%4
            self.data = self.type[self.turn]

    def hard_drop(self):
        ypos = self.ypos
        while not is_overlapped(self.xpos, ypos+1, self.turn):
            ypos = ypos + 1
        self.ypos = ypos


def erase_line():
    erased = 0
    ypos = HEIGHT-1
    while ypos >= 0:
        if FIELD[ypos].count('B') == 0 and FIELD[ypos].count('W') == 2:
            erased = erased + 1
            del FIELD[ypos]
            new_line = ['B']*(WIDTH-2)
            new_line.insert(0, 'W')
            new_line.append('W')
            FIELD.insert(0, new_line)
        else:
            ypos = ypos - 1
    return erased


def is_game_over():
    filled = 0
    for cell in FIELD[0]:
        if cell != 'B':
            filled += 1
    return filled > 2


def get_block():
    global BLOCK_QUEUE
    # 현대 테스리스는 모든 블록이 1번씩 무작위로 순회
    while len(BLOCK_QUEUE) < len(BLOCKS.keys())+1:
        new_blocks = list()
        for name in BLOCKS.keys():
            new_blocks.append(Block(name))
        random.shuffle(new_blocks)
        BLOCK_QUEUE.extend(new_blocks)
    return BLOCK_QUEUE.pop(0)


def is_overlapped(xpos, ypos, turn):
    data = BLOCK.type[turn]
    for y_offset in range(BLOCK.size):
        for x_offset in range(BLOCK.size):
            if ((0 <= xpos+x_offset < WIDTH) and
                (0 <= ypos+y_offset < HEIGHT)):
                if ((data[y_offset*BLOCK.size + x_offset] != 'B') and
                    (FIELD[ypos+y_offset][xpos+x_offset] != 'B')):
                    return True
    return False

# 전역 변수
pygame.init()
pygame.key.set_repeat(30, 30)
SURFACE = pygame.display.set_mode([600, 600])
FPSCLOCK = pygame.time.Clock()
WIDTH = 10 + 2
HEIGHT = 20 + 1
FIELD = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
BLOCK = None
BLOCK_QUEUE = list()
FPS = 15
DIFFICULT = 1


def main():
    global BLOCK
    global DIFFICULT
    score = 0
    # 초기화
    if BLOCK is None:
        BLOCK = get_block()

    # 메시지
    smallfont = pygame.font.SysFont(None, 36)
    largefont = pygame.font.SysFont(None, 72)
    message_over = largefont.render("GAME OVER!!",
                                    True, (255, 255, 255))
    message_rect = message_over.get_rect()
    message_rect.center = (300, 300)

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

        # 게임 오버 확인
        if is_game_over():
            SURFACE.blit(message_over, message_rect)
        else: ## 게임 오버가 아님
            # 움직임 처리
            if key == K_UP:
                BLOCK.up()
            elif key == K_RIGHT:
                BLOCK.right()
            elif key == K_LEFT:
                BLOCK.left()
            elif key == K_DOWN:
                BLOCK.down()
            elif key == K_SPACE:
                BLOCK.hard_drop()

            # Draw FIELD
            SURFACE.fill((0, 0, 0))
            for ypos in range(HEIGHT):
                for xpos in range(WIDTH):
                    value = FIELD[ypos][xpos]
                    pygame.draw.rect(SURFACE, COLORS[value],
                                     (xpos*25 + 25, ypos*25 + 25, 24, 24))

            # Landing and erase line
            erased = BLOCK.update()
            if erased > 0:
                score = score + 2**erased
                DIFFICULT = min(ceil(score/10), 15)
            BLOCK.draw()

            # Draw Next BLOCKS
            ymargin = 0
            for next_block in BLOCK_QUEUE[0:7]:
                ymargin = ymargin + 1
                for ypos in range(next_block.size):
                    for xpos in range(next_block.size):
                        value = next_block.data[xpos+ypos*next_block.size]
                        pygame.draw.rect(SURFACE, COLORS[value],
                                         (xpos*15+460, ypos*15+75*ymargin, 
                                          15, 15))

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

