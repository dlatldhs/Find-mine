#pygame과 random 을 import 해서 불러줍니당
import pygame
import random

#pygame 초기화 해주기
pygame.init() 

# ☆POINT☆
#  지뢰 게임의 핵심
#  2차원 배열을 만들어(셀)
#  2차원 배열 안에 지뢰를 넣는 것이 구현의 포인트임

#전역 변수 선언하기

#=======색깔=============
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
#=======색깔=============
#=======게임-폰트-설정=====================
large_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)
#=======게임-폰트-설정=====================

#===========display-size==================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#===========display-size==================

#CELL_SIZE 가로 셀 과 세로 셀 에 들어갈 지뢰의 개수
CELL_SIZE = 50
COLUMN_COUNT = SCREEN_WIDTH // CELL_SIZE
ROW_COUNT = SCREEN_HEIGHT // CELL_SIZE
#================================================

#=============================================================GRID 라는 리스트를 만들어서==============================================
# mine = 지뢰의 여부 
# open은 활성화 여부
# mine_count_around는 주변의 지뢰 개수 
# flag 는 flag활성화 여부 
grid = [[{'mine': False, 'open': False, 'mine_count_around': 0, 'flag': False} for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]
#======================================================================================================================================

MINE_COUNT = 15

for _ in range(MINE_COUNT):
    while True:
        #가로 세로 지뢰 랜덤하게 index 정하는 거 =========
        column_index = random.randint(0, COLUMN_COUNT - 1)
        row_index = random.randint(0, ROW_COUNT - 1)
        #=================================================
        tile = grid[row_index][column_index]

        #리스트안에 지뢰가 없으면 실행해서 지뢰를안에 넣음 
        if not tile['mine']:
            tile['mine'] = True 
            break

clock = pygame.time.Clock() 
