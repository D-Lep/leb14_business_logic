import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Tic-Tac-Toe")
clock = pygame.time.Clock()
running = True

fild = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

player = 1
winner = 0
is_game = True

def check_game_end():
    global is_game, winner
    
    for k in range(3):
        if fild[k][0] == fild[k][1] == fild[k][2] != 0:
            winner = fild[k][0]
            is_game = False
            return
        if fild[0][k] == fild[1][k] == fild[2][k] != 0:
            winner = fild[0][k]
            is_game = False
            return

    if fild[0][0] == fild[1][1] == fild[2][2] != 0:
        winner = fild[0][0]
        is_game = False
        return
    if fild[0][2] == fild[1][1] == fild[2][0] != 0:
        winner = fild[0][2]
        is_game = False
        return

    is_free_space = False
    for i in range(3):
        for j in range(3):
            if fild[i][j] == 0:
                is_free_space = True
                break
        if is_free_space:
            break

    if not is_free_space:
        winner = 0  # Нічия
        is_game = False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == MOUSEBUTTONUP and is_game:
            if event.button == 1:
                x, y = event.pos
                fi, fj = -1, -1
                
                if 10 <= x <= 210:
                    fi = 0
                elif 220 <= x <= 420:
                    fi = 1
                elif 430 <= x <= 630:
                    fi = 2

                if 10 <= y <= 210:
                    fj = 0
                elif 220 <= y <= 420:
                    fj = 1
                elif 430 <= y <= 630:
                    fj = 2

                if fi == -1 or fj == -1:   
                    continue
                if fild[fi][fj] != 0:   
                    continue

                if player == 1:
                    fild[fi][fj] = 1
                    player = 2
                elif player == 2:
                    fild[fi][fj] = 2
                    player = 1
                
                check_game_end()

    screen.fill("white")

    for i in range(3):
        for j in range(3):
            color = "black"
            width = 5
            
            pygame.draw.rect(screen, color, ((i + 1) * 10 + i * 200, (j + 1) * 10 + j * 200, 200, 200), width)
            
            if fild[i][j] == 1:
                x_pos = (i + 1) * 10 + i * 200 + 20
                y_pos = (j + 1) * 10 + j * 200 + 20
                pygame.draw.line(screen, 'red', (x_pos, y_pos), (x_pos + 160, y_pos + 160), 15)
                pygame.draw.line(screen, 'red', (x_pos, y_pos + 160), (x_pos + 160, y_pos), 15)
                
            elif fild[i][j] == 2:
                x_pos = (i + 1) * 10 + i * 200 + 100
                y_pos = (j + 1) * 10 + j * 200 + 100
                pygame.draw.circle(screen, 'blue', (x_pos, y_pos), 80, 15)

    if is_game is False:
        text = 'Game Over! '
        color = 'black'
        if winner == 1:
            text += "Player 1 win!"
            color = 'red'
        elif winner == 2:
            text += "Player 2 win!"
            color = 'blue'
        else:
            text += "Draw!"
            color = 'purple'

        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render(text, False, color, 'white')
        screen.blit(text_surface, (180, 300))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()