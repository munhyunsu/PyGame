import sys
from math import sqrt
import random

import pygame
from pygame.locals import QUIT, KEYDOWN, K_UP, K_LEFT, K_RIGHT, K_DOWN, K_SPACE, K_ESCAPE

from material import *


class Block: # 객체 갱신 필요
    """ 블록 객체 """
    def __init__(self, name):
        self.turn = 0
        self.type = BLOCKS[name]
        self.data = self.type[self.turn]
        self.size = int(sqrt(len(self.data))) 
        self.xpos = 4
        self.ypos = 1 - self.size
        self.stop = 0

    def update(self):
        global BLOCK
        """ 블록 상태 갱신 (소거한 단의 수를 반환한다) """
        # 아래로 총돌?
        erased = 0
        if is_overlapped(self.xpos, self.ypos+1, self.turn):
            for y_offset in range(self.size):
                for x_offset in range(self.size):
                    if 0 <= self.xpos+x_offset < WIDTH and \
                        0 <= self.ypos+y_offset < HEIGHT:
                        val = self.data[y_offset*self.size \
                                            + x_offset]
                        if val != 'B':
                            FIELD[self.ypos+y_offset]\
                                 [self.xpos+x_offset] = val

            BLOCK = get_block()
#            erased = erase_line()
        
        else:
            self.stop = self.stop + 1
            if self.stop > FPS/DIFFICULT:
                self.stop = 0
                self.ypos = self.ypos + 1
#        return erased

    def draw(self):
        """ 블록을 그린다 """
        for index in range(len(self.data)):
            xpos = index % self.size
            ypos = index // self.size
            val = self.data[index]
            if 0 <= ypos + self.ypos < HEIGHT and \
               0 <= xpos + self.xpos < WIDTH and val != 'B':
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


def erase_line():
    """ 행이 모두 찬 단을 지운다 """
    erased = 0
    ypos = 20
    while ypos >= 0:
        if all(FIELD[ypos]):
            erased += 1
            del FIELD[ypos]
            FIELD.insert(0, [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8])
        else:
            ypos -= 1
    return erased

def is_game_over():
    """ 게임 오버인지 아닌지 """
    filled = 0
    for cell in FIELD[0]:
        if cell != 'B':
            filled += 1
    return filled > 2   # 2 = 좌우의 벽

def go_next_block(count):
    global BLOCK, NEXT_BLOCK, BLOCK_QUEUE
    if len(BLOCK_QUEUE) == 0:
        for name in BLOCKS.keys():
            BLOCK_QUEUE.append(Block(name))
        random.shuffle(BLOCK_QUEUE)
    if NEXT_BLOCK is None:
        NEXT_BLOCK = BLOCK_QUEUE.pop(0)
    BLOCK = NEXT_BLOCK
    NEXT_BLOCK = BLOCK_QUEUE.pop(0)



def get_block():
    global BLOCK_QUEUE
    # 현대 테스리스는 모든 블록이 1번씩 무작위로 순회합니다.
    while len(BLOCK_QUEUE) < len(BLOCKS.keys())+1:
        new_blocks = list()
        for name in BLOCKS.keys():
            new_blocks.append(Block(name))
        random.shuffle(new_blocks)
        BLOCK_QUEUE.extend(new_blocks)
    return BLOCK_QUEUE.pop(0)


def is_overlapped(xpos, ypos, turn):
    """ 블록이 벽이나 땅의 블록과 충돌하는지 아닌지 """
    data = BLOCK.type[turn]
    for y_offset in range(BLOCK.size):
        for x_offset in range(BLOCK.size):
            if 0 <= xpos+x_offset < WIDTH and \
                0 <= ypos+y_offset < HEIGHT:
                if data[y_offset*BLOCK.size + x_offset] != 'B' and \
                    FIELD[ypos+y_offset][xpos+x_offset] != 'B':
                    return True
    return False

# 전역 변수
pygame.init()
pygame.key.set_repeat(30, 30)
SURFACE = pygame.display.set_mode([600, 600])
FPSCLOCK = pygame.time.Clock()
WIDTH = 10 + 2
HEIGHT = 20 + 1
INTERVAL = 40
FIELD = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
BLOCK = None
NEXT_BLOCK = None
BLOCK_QUEUE = list()
FPS = 15
DIFFICULT = 3


def main():
    """ 메인 루틴 """
    global INTERVAL
    global BLOCK
    count = 0
    score = 0
    game_over = False
    smallfont = pygame.font.SysFont(None, 36)
    largefont = pygame.font.SysFont(None, 72)
    message_over = largefont.render("GAME OVER!!",
                                    True, (0, 255, 225))
    message_rect = message_over.get_rect()
    message_rect.center = (300, 300)

    # 필드를 숫자로 나타낼 것인데, 8은 벽을 의미합니다.
    for ypos in range(HEIGHT):
        for xpos in range(WIDTH):
            FIELD[ypos][xpos] = 'W' if xpos == 0 or \
                xpos == WIDTH - 1 else 'B'
    for index in range(WIDTH):
        FIELD[HEIGHT-1][index] = 'W'

    # 초기화
    if BLOCK is None:
        BLOCK = get_block()

    # 게임 무한 루프를 수행
    while True:
        # 이벤트 루프를 확인
        ## 게임오버가 되면 게임내 이벤트 처리를 막아야하기 때문에
        ## 이벤트 루프 확인 구간에서는 '종료' 처리 및 '입력 키' 저장 수행
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

            # Draw FIELD
            SURFACE.fill((0, 0, 0))
            for ypos in range(HEIGHT):
                for xpos in range(WIDTH):
                    value = FIELD[ypos][xpos]
                    pygame.draw.rect(SURFACE, COLORS[value],
                                     (xpos*25 + 25, ypos*25 + 25, 24, 24))

            BLOCK.update()
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

        # Erase lines
#        erased = BLOCK.update()
#        if erased > 0 :
#            score = score + 2**erased

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

