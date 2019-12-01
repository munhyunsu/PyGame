import sys

import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

from material import *

# 전역 변수
pygame.init()
SURFACE = pygame.display.set_mode([600, 600])
FPSCLOCK = pygame.time.Clock()
WIDTH = 10 + 2
HEIGHT = 20 + 1
FIELD = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
FPS = 15


def main():
    score = 0
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

        # Draw FIELD
        SURFACE.fill((0, 0, 0))
        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                value = FIELD[ypos][xpos]
                pygame.draw.rect(SURFACE, COLORS[value],
                                 (xpos*25 + 25, ypos*25 + 25, 24, 24))

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

