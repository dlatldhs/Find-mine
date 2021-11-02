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

# 마우스 포인터를 이용해서 마우스에 접근 함==============================
# 마우스가 셀 안에 있는 건지 확인을 해주는 함수
def in_bound(column_index, row_index):
    if (0 <= column_index < COLUMN_COUNT and 0 <= row_index < ROW_COUNT):
        return True
    else:
        return False
#========================================================================


def open_tile(column_index, row_index): 
    if not in_bound(column_index, row_index):# 셀 안에 있는 거면 1이 리턴되는데 그게 not 반대니까 0 이라서 실행이 안됨
        return

    tile = grid[row_index][column_index]
    #셀이 열려있지 않으면 활성화 True
    if not tile['open']:
        tile['open'] = True
    #아니면 리턴
    else:    
        return

    #지뢰면 리턴 
    if tile['mine']:
        return

    #주변의 지뢰 개수를 리턴 함    
    #밑에 함수 실행 후 주변의 ☆비어 있는 셀☆ 들을 전부 오픈 함
    mine_count_around = get_mine_count_around(column_index, row_index)
    if mine_count_around > 0:
        tile['mine_count_around'] = mine_count_around
    else:
        for dc, dr in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            column_index_around, row_index_around = (column_index + dc, row_index + dr)
            open_tile(column_index_around, row_index_around)

# 그 블록을 중심으로 9칸을 다 둘러보고 지뢰가 몇 개 있는지 계산해서 결과를 리턴해서 셀에다가 나타냄
def get_mine_count_around(column_index, row_index):
    count = 0

    for dc, dr in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        column_index_around, row_index_around = (column_index + dc, row_index + dr)
        if in_bound(column_index_around, row_index_around) and grid[row_index_around][column_index_around]['mine']:
            count += 1
    return count
#===============================================사용할-함수들-끝======================================================

def runGame():
    SUCCESS = 1
    FAILURE = 2
    game_over = 0
 
    while True: 
        clock.tick(30) 
        screen.fill(BLACK) 
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                column_index = event.pos[0] // CELL_SIZE
                row_index = event.pos[1] // CELL_SIZE
                if event.button == 1:
                    if in_bound(column_index, row_index):
                        tile = grid[row_index][column_index]
                        if tile['mine']:
                            tile['open'] = True
                            game_over = FAILURE
                        else:
                            open_tile(column_index, row_index)
                elif event.button == 3:
                    if in_bound(column_index, row_index):
                        tile = grid[row_index][column_index]
                        if not tile['flag']:
                            tile['flag'] = True
                        else:
                            tile['flag'] = False
 
                        success = True
                        for row_index in range(ROW_COUNT):
                            for column_index in range(COLUMN_COUNT):
                                tile = grid[row_index][column_index]
                                if tile['mine'] and not tile['flag']:
                                    success = False
                                    break
                        if success:
                            game_over = SUCCESS
        for column_index in range(COLUMN_COUNT):
            for row_index in range(ROW_COUNT):
                tile = grid[row_index][column_index]
                if tile['mine_count_around']:
                    mine_count_around_image = small_font.render('{}'.format(tile['mine_count_around']), True, YELLOW)
                    screen.blit(mine_count_around_image, mine_count_around_image.get_rect(centerx=column_index * CELL_SIZE + CELL_SIZE // 2, centery=row_index * CELL_SIZE + CELL_SIZE // 2))
                if tile['mine']: 
                    mine_image = small_font.render('x', True, RED)
                    screen.blit(mine_image, mine_image.get_rect(centerx=column_index * CELL_SIZE + CELL_SIZE // 2, centery=row_index * CELL_SIZE + CELL_SIZE // 2)) #지뢰 설치
                if not tile['open']:
                    pygame.draw.rect(screen, GRAY, pygame.Rect(column_index * CELL_SIZE, row_index * CELL_SIZE, CELL_SIZE, CELL_SIZE)) #커버
                if tile['flag']: 
                    v_image = small_font.render('v', True, WHITE)
                    screen.blit(v_image, (column_index * CELL_SIZE + 10, row_index * CELL_SIZE + 10)) 
                pygame.draw.rect(screen, WHITE, pygame.Rect(column_index * CELL_SIZE, row_index * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        if game_over > 0:
            if game_over == SUCCESS:
                success_image = large_font.render('Success', True, RED)
                screen.blit(success_image, success_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))
            elif game_over == FAILURE:
                failure_image = large_font.render('Failure', True, RED)
                screen.blit(failure_image, failure_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))

        pygame.display.update() 

runGame()
pygame.quit()