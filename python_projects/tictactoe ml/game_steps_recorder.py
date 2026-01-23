import pygame as pg
import pandas as pd
import os

SIDE = 500
display = pg.display.set_mode((SIDE+150,SIDE),pg.SCALED)
clock = pg.time.Clock()
divisions = 3
gap = SIDE/divisions
x,y = -10,-10
grid = [
    [0,0,0],
    [0,0,0],
    [0,0,0]
]
chance = 1

feed_data = {"1 1":[],"1 2":[],"1 3":[],"2 1":[],"2 2":[],"2 3":[],"3 1":[],"3 2":[],"3 3":[],"decision":[]}

def botton_clicked(mx,my,x,y,w,h):
    if not x < mx < w+x:
        return 0
    if not y < my < h+y:
        return 0
    return 1

def update_feed(grid,x,y):
    global feed_data
    for y1 in range(divisions):
        for x1 in range(divisions):
            feed_data[f"{y1+1} {x1+1}"].append(grid[y1][x1])
    feed_data["decision"].append(f"{y} {x}")

padding = 10
while 1:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
        if e.type == pg.MOUSEBUTTONDOWN:
            x,y = pg.mouse.get_pos()
            if x < SIDE:
                x = x/SIDE*100
                y = y/SIDE*100
                chance = 2 if chance == 1 else 1
                for i in range(divisions):
                    if (i+1)*gap/SIDE*100 > x:
                        x = i
                        break
                for i in range(divisions):
                    if (i+1)*gap/SIDE*100 > y:
                        y = i
                        break
                if chance == 2:
                    update_feed(grid,x+1,y+1)
                grid[y][x] = chance
            else:
                clicked = botton_clicked(x,y,SIDE+30,0.3*SIDE,(SIDE+150)-(SIDE+60),100)
                if clicked:
                    if os.path.exists("tictactoe.csv"):
                        df = pd.read_csv("tictactoe.csv")
                        a = pd.DataFrame(feed_data)

                        df = pd.concat([df, a], ignore_index=True)
                        df.to_csv("tictactoe.csv", index=False)
                    else:
                        a = pd.DataFrame(feed_data)
                        a.to_csv("tictactoe.csv", index=False)

                    print("SAVED !!")

        if e.type == pg.MOUSEBUTTONUP:
            x,y = -10,-10

    display.fill((147, 81, 4))


    for i in range(2):
        pg.draw.line(display,(111, 60, 0),((i+1)*gap,0),((i+1)*gap,SIDE),5)
        pg.draw.line(display, (111, 60, 0), (0,(i + 1) * gap), (SIDE,(i + 1) * gap),5)
    pg.draw.line(display, (111, 60, 0), (divisions*gap, 0), (divisions*gap, SIDE), 5)
    for y in range(divisions):
        for x in range(divisions):
            if grid[y][x] == 1:
                pg.draw.rect(display, (0, 76, 138), pg.Rect(x * gap + padding, y * gap + padding, gap-2*padding, gap-2*padding))
            elif grid[y][x] == 2:
                pg.draw.rect(display,(184, 60, 47),pg.Rect(x * gap + padding, y * gap + padding, gap-2*padding, gap-2*padding))
    pg.draw.rect(display,(6, 218, 63),pg.Rect(SIDE+30,0.3*SIDE,(SIDE+150)-(SIDE+60),100))
    pg.display.flip()
    clock.tick(60)
