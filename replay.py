import pygame as pg
from main import Board
import json
from datetime import datetime as dt

if __name__ == "__main__":
    pg.init()
    WIN = pg.display.set_mode((800, 600), pg.RESIZABLE)
    pg.display.set_caption("2048 Drop Replay")
    with open("replays.json", "r") as f:
        data = json.load(f)

    recent = list(
        max(data.items(), key=lambda kv: dt.strptime(kv[0], "%y/%m/%d %H:%M.%S"))
    )

    states = recent[1]

    BOARD = Board(WIN)
    elements = pg.sprite.Group(BOARD)

    playing = True
    timestamp = 0

    clock = pg.time.Clock()

    while True:
        delta = clock.tick(60)
        if pg.mouse.get_pos()[1] > BOARD.rect.height * 0.8:
            playing = False
        else:
            playing = True
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pass
            if event.type == pg.MOUSEMOTION:
                if not playing:
                    timestamp = int(
                        (event.pos[0] / BOARD.rect.width) * float(max(states.keys()))
                    )

        if playing:
            timestamp += delta

        WIN.fill((255, 255, 255))

        nearest_stamp = min(states.keys(), key=lambda x: abs(int(x) - int(timestamp)))
        print(timestamp / 1000, int(nearest_stamp) / 1000)
        BOARD.board = states[nearest_stamp]
        elements.update()
        elements.draw(WIN)
        pg.display.update()
