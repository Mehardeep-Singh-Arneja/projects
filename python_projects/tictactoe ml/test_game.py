import pygame as pg
import joblib
import numpy as np
import pandas as pd

model = joblib.load("model.pkl")

SIDE = 500
display = pg.display.set_mode((SIDE + 150, SIDE), pg.SCALED)
clock = pg.time.Clock()

divisions = 3
gap = SIDE / divisions
padding = 10

grid = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

BOT = 1
HUMAN = 2
turn = BOT

def board_to_list(grid):
    return [grid[r][c] for r in range(3) for c in range(3)]

def predict_move(board):
    X = pd.DataFrame([board])
    probs = model.predict_proba(X)[0]
    classes = model.classes_
    ranked = np.argsort(probs)[::-1]

    for idx in ranked:
        if board[idx] == 0:
            return idx
    return None

def bot_play():
    global turn
    board = board_to_list(grid)
    idx = predict_move(board)
    if idx is not None:
        r, c = divmod(idx, 3)
        grid[r][c] = BOT
    turn = HUMAN

def human_play(mx, my):
    global turn
    x = int(mx // gap)
    y = int(my // gap)
    if 0 <= x < 3 and 0 <= y < 3 and grid[y][x] == 0:
        grid[y][x] = HUMAN
        turn = BOT

def draw_grid():
    for i in range(2):
        pg.draw.line(display, (111, 60, 0), ((i+1)*gap, 0), ((i+1)*gap, SIDE), 5)
        pg.draw.line(display, (111, 60, 0), (0, (i+1)*gap), (SIDE, (i+1)*gap), 5)

    for y in range(3):
        for x in range(3):
            if grid[y][x] == BOT:
                pg.draw.rect(
                    display, (0, 76, 138),
                    pg.Rect(x*gap+padding, y*gap+padding, gap-2*padding, gap-2*padding)
                )
            elif grid[y][x] == HUMAN:
                pg.draw.rect(
                    display, (184, 60, 47),
                    pg.Rect(x*gap+padding, y*gap+padding, gap-2*padding, gap-2*padding)
                )

pg.display.set_caption("Tic Tac Toe – Player vs ML Bot")

bot_play()  # bot plays first

running = True
while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

        if e.type == pg.MOUSEBUTTONDOWN and turn == HUMAN:
            mx, my = pg.mouse.get_pos()
            if mx < SIDE:
                human_play(mx, my)

    if turn == BOT:
        pg.time.delay(300)
        bot_play()

    display.fill((147, 81, 4))
    draw_grid()
    pg.display.flip()
    clock.tick(60)

pg.quit()
