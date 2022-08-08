

import math
import sys
from turtle import Screen
import pygame as pg
import numpy as np
from cProfile import label


ROW_COUNT = 6
COLUMN_COUNT = 7
COLOR = (64, 224, 208)
CIRCLECOLOR = (72, 61, 139)
P1COLOR = (220, 20, 60)
P2COLOR = (210, 105, 30)


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def wining_move(board, piece):

    # for Horizontal picecs
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

# for Vertical pieces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

# for postive diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

# for negative diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][r+3] == piece:
                return True


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pg.draw.rect(screen, COLOR, (c * SQUARESIZE, r *
                         SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pg.draw.circle(screen, CIRCLECOLOR, (int(c * SQUARESIZE + SQUARESIZE/2),
                           int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pg.draw.circle(screen, P1COLOR, (int(
                    c * SQUARESIZE + SQUARESIZE/2), height - int(r * SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pg.draw.circle(screen, P2COLOR, (int(
                    c * SQUARESIZE + SQUARESIZE/2), height - int(r * SQUARESIZE + SQUARESIZE/2)), RADIUS)
    pg.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

pg.init()
# squaresize
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 3)

screen = pg.display.set_mode(size)
draw_board(board)
pg.display.update()

myfont = pg.font.SysFont("monospace", 75)

while not game_over:

    for event in pg.event.get():
        # if event.type == pg.QUIT:
        #     sys.exit()

        if event.type == pg.MOUSEMOTION:
            pg.draw.rect(screen, COLOR,  (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pg.draw.circle(screen, P1COLOR,
                               (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pg.draw.circle(screen, P2COLOR,
                               (posx, int(SQUARESIZE/2)), RADIUS)
        pg.display.update()

        if event.type == pg.MOUSEBUTTONDOWN:
            pg.draw.rect(screen, COLOR,  (0, 0, width, SQUARESIZE))
            # print(event.pos)
            if turn == 0:
                turn += 1
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if wining_move(board, 1):
                        label = myfont.render("Player 1 wins!!!", 1, P1COLOR)
                        screen.blit(label, (40,10))
                        game_over = True

            else:
                turn -= 1
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col,)
                    drop_piece(board, row, col, 2)

                    if wining_move(board, 2):
                        label = myfont.render("Player 2 wins!!!", 1, P2COLOR)
                        screen.blit(label, (40,10))
                        game_over = True

            print_board(board)
            draw_board(board)

            if game_over:
                pg.time.wait(3000)
