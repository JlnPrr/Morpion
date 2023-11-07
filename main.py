import pygame
import random
import math
from math import inf as infinity
import sys
import os
import time
from pygame import mixer


pygame.init()
pygame.font.init()



Width, Height = 670,670

Win = pygame.display.set_mode((Width, Height))

Cross = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "cross.png")), (Width//3, Height//3))
Circle = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "circle.png")), (Width//3, Height//3))


Bg = (95, 114, 122)
Clock = pygame.time.Clock()

pygame.display.set_caption("Morpion")
windowIcon = pygame.image.load("Assets/tac_tic_toe_icon.png")
pygame.display.set_icon(windowIcon)

mixer.music.load("Assets/Of Far Different Nature - Liquid Flame (CC0).mp3")
mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

AI = +1
Human = -1


FPS = 120

def fill(surface, color):
    w,h = surface.get_size()
    r,g,b,_ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x,y))[3]
            surface.set_at((x,y), pygame.Color(r,g,b,a))


def create_board():
    new_board = [[0 for i in range(3)] for j in range(3)]
    return new_board

def check_game(board, player):

    for row in board:
        if row[0] == row[1] == row[2] == player:
            print(player, "gagne")
            return True

    for col in range(len(board)):
        check = []

        for row in board:
            check.append(row[col])
        if check.count(player) == len(check) and check[0] != 0:
            print("player", player, "gagne")
            return True

    diags = []
    for indx in range(len(board)):
        diags.append(board[indx][indx])
    if diags.count(player) == len(diags) and diags[0] != 0:
        print(player, "gagne")
        return True

    diags_2 = []
    for indx, rev_indx in enumerate(reversed(range(len(board)))):
        diags_2.append(board[indx][rev_indx])
    if diags_2.count(player) == len(diags_2) and diags_2[0] != 0:
        print(player, "gagne")
        return True


    if len(empty_cells(board)) == 0:
        print("personne ne gagne")
        return True


def empty_cells(board):
    empty_cells = []
    for y,row in enumerate(board):
        for x,case in enumerate(row):
            if case == 0:
                empty_cells.append([x,y])

    return empty_cells

def is_terminal_node(board):
    return check_game(board, +1) or check_game(board, -1)

def evaluate(board):
    if check_game(board, 1):
        score = 5
    elif check_game(board, -1):
        score = -5
    else:
        score = 0

    return score


def minimax(board, depth, alpha, beta, player):
    if player == AI:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or is_terminal_node(board):
        score = evaluate(board)
        return [-1, -1, score]

    for location in empty_cells(board):
        x,y = location[0], location[1]
        board[y][x] = player
        info = minimax(board, depth-1, alpha, beta, -player)
        board[y][x] = 0
        info[0], info[1] = x,y

        if player == AI:
            if info[2] > best[2]:
                best = info

            alpha = max(alpha, best[2])
            if alpha >= beta:
                break

        else:
            if best[2] > info[2]:
                best = info
            beta = min(beta, best[2])
            if alpha >= beta:
                break

    return best


def ai_turn(board, alpha, beta):
    depth = len(empty_cells(board))

    if depth == 0 or is_terminal_node(board):
        return

    if depth == 9:
        x = random.choice([0,1,2])
        y = random.choice([0,1,2])
    else:
        move = minimax(board, depth, alpha, beta, AI)
        x,y = move[0], move[1]

    set_locations(board, x,y, AI)


def valid_locations(board, x, y, player):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_locations(board, x, y, player):
    if valid_locations(board, x, y, player):
        board[y][x] = player
        return True

    else:
        return False

def draw_board(Win):
    for i in range(1, 3):
        pygame.draw.line(Win, (255, 255, 255), (Width*(i/3), 0), (Width*(i/3), Height), 1)

    for j in range(1,3):
        pygame.draw.line(Win, (255, 255, 255), (0, Width*(j/3)), (Width, Width*(j/3)), 1)


def draw_pieces(Win, board):
    for x in range(len(board)):
        for y in range(len(board)):
            if board[y][x] == -1:
                Win.blit(Circle, (x*(Width//3), y*(Width//3)))
            elif board[y][x] == 1:
                Win.blit(Cross, (x*(Width//3), y*(Width//3)))

def reset_board(board):
    for x,row in enumerate(board):
        for y in range(len(row)):
            board[y][x] = 0


def redraw_window(Win, board):
    Win.fill(Bg)
    draw_board(Win)
    draw_pieces(Win, board)

    pygame.display.update()

def main():
    run = True
    turn = random.choice([-1, 1])
    game_over = False
    game_board = create_board()
    green = (0, 255, 0, 0)

    while run:
        fill(Circle,green)
        redraw_window(Win, game_board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    reset_board(game_board)
                    main()

            if event.type == pygame.MOUSEBUTTONDOWN and turn == Human and not game_over:

                pos = pygame.mouse.get_pos()
                if turn == Human and not game_over:
                    if set_locations(game_board,pos[0]//(Width//3), pos[1]//(Width//3), turn):
                        if check_game(game_board, Human):
                            print("terminé")
                            game_over = True
                        turn = AI

        if turn == AI and not game_over:
            alpha = -infinity
            beta = +infinity
            ai_turn(game_board, alpha, beta)
            if check_game(game_board, AI):
                game_over = True

            turn = Human


main()
