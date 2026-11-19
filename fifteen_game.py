import pygame
import random
from pygame.locals import *

pygame.init()
pygame.font.init()
pygame.display.set_caption('П’ятнашки (Fifteen)')
screen = pygame.display.set_mode((640, 640))
clock = pygame.time.Clock()

mode = 0  
steps = 0

field = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0]
]

def get_empty_cell():
    for i in range(4):
        for j in range(4):
            if field[i][j] == 0:
                return i, j
    return 0, 0

def shuffle_field():
    global field
    field = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]
    for _ in range(150):
        empty_i, empty_j = get_empty_cell()
        valid_moves = []
        if empty_i > 0: valid_moves.append((empty_i - 1, empty_j))
        if empty_i < 3: valid_moves.append((empty_i + 1, empty_j))
        if empty_j > 0: valid_moves.append((empty_i, empty_j - 1))
        if empty_j < 3: valid_moves.append((empty_i, empty_j + 1))
        
        mi, mj = random.choice(valid_moves)
        field[empty_i][empty_j], field[mi][mj] = field[mi][mj], field[empty_i][empty_j]

def detect_cell(x, y):
    fi, fj = -1, -1
    cell_size = 135
    gap = 12
    margin = 20
    
    for i in range(4):
        cx = margin + i * (cell_size + gap)
        if cx <= x <= cx + cell_size:
            fi = i
            break
            
    for j in range(4):
        cy = margin + j * (cell_size + gap)
        if cy <= y <= cy + cell_size:
            fj = j
            break
            
    return fi, fj

def check_win():
    winning_field = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]
    return field == winning_field

def draw_content():
    screen.fill((245, 245, 245))
    my_font = pygame.font.SysFont('Comic Sans MS', 36)
    title_font = pygame.font.SysFont('Comic Sans MS', 48)
    
    if mode == 0:
        text_surface = title_font.render('Гра "П’ятнашки"', False, 'darkblue', (245, 245, 245))
        screen.blit(text_surface, (165, 200))
        
        prompt_surface = my_font.render('Клікніть, щоб почати гру', False, 'dimgray', (245, 245, 245))
        screen.blit(prompt_surface, (130, 280))
        
    elif mode == 1:
        cell_size = 135
        gap = 12
        margin = 20
        
        for i in range(4):
            for j in range(4):
                val = field[i][j]
                x = margin + i * (cell_size + gap)
                y = margin + j * (cell_size + gap)
                
                if val != 0:
                    pygame.draw.rect(screen, (70, 130, 180), (x, y, cell_size, cell_size), border_radius=8)
                    pygame.draw.rect(screen, 'black', (x, y, cell_size, cell_size), 3, border_radius=8)
                    
                    num_surf = my_font.render(str(val), True, 'white')
                    text_rect = num_surf.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
                    screen.blit(num_surf, text_rect)
                else:
                    pygame.draw.rect(screen, (210, 210, 210), (x, y, cell_size, cell_size), border_radius=8)
                    
        steps_surf = my_font.render(f'Кроки: {steps}', True, 'black')
        screen.blit(steps_surf, (20, 590))
        
    elif mode == 2:
        text_surface = title_font.render('Перемога!', False, 'forestgreen', (245, 245, 245))
        screen.blit(text_surface, (210, 180))
        
        res_text = f'Зроблено кроків: {steps}'
        res_surface = my_font.render(res_text, True, 'black', (245, 245, 245))
        screen.blit(res_surface, (170, 260))
        
        prompt_surface = my_font.render('Клікніть, щоб грати знову', False, 'dimgray', (245, 245, 245))
        screen.blit(prompt_surface, (135, 340))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if mode == 0:
                    mode = 1
                    steps = 0
                    shuffle_field()
                elif mode == 1:
                    x, y = event.pos
                    ci, cj = detect_cell(x, y)
                    
                    if ci != -1 and cj != -1:
                        empty_i, empty_j = get_empty_cell()
                        if abs(ci - empty_i) + abs(cj - empty_j) == 1:
                            field[empty_i][empty_j] = field[ci][cj]
                            field[ci][cj] = 0
                            steps += 1
                            
                            if check_win():
                                mode = 2
                elif mode == 2:
                    mode = 1
                    steps = 0
                    shuffle_field()
                    
    draw_content()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()