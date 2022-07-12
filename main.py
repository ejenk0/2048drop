import pygame as pg
import numpy as np
import random as rd
from datetime import datetime as dt
import json

pg.init()

WIN = pg.display.set_mode((1000, 700), pg.RESIZABLE)
pg.display.set_caption("2048 Drop")


class Board(pg.sprite.Sprite):
    def __init__(self, win: pg.Surface):
        super().__init__()
        self.win = win
        self.reset()

        # self.board[4] = [32768, 65536, 131072, 262144, 524288, 1048576, 2097152]
        # self.board[5] = [256, 512, 1024, 2048, 4096, 8192, 16384]
        # self.board[6] = [2, 4, 8, 16, 32, 64, 128]

        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)

        # Original game
        # self.tilecolours = {
        #     "2": {"bg": (237, 228, 218), "text": BLACK},
        #     "4": {"bg": (237, 224, 199), "text": BLACK},
        #     "8": {"bg": (242, 177, 120), "text": WHITE},
        #     "16": {"bg": (244, 148, 99), "text": WHITE},
        #     "32": {"bg": (246, 123, 96), "text": WHITE},
        #     "64": {"bg": (245, 94, 59), "text": WHITE},
        #     "128": {"bg": (237, 207, 114), "text": WHITE},
        #     "246": {"bg": (236, 204, 96), "text": WHITE},
        #     "512": {"bg": (236, 200, 81), "text": WHITE},
        #     "1024": {"bg": (237, 200, 60), "text": WHITE},
        #     "2048": {"bg": (236, 193, 46), "text": WHITE},
        #     "4096": {"bg": (61, 57, 50), "text": WHITE},
        # }

        self.tilecolours = {
            "2": {"bg": (237, 228, 218), "text": BLACK},
            "4": {"bg": (237, 216, 161), "text": BLACK},
            "8": {"bg": (236, 205, 103), "text": WHITE},
            "16": {"bg": (236, 193, 46), "text": WHITE},
            "32": {"bg": (235, 154, 38), "text": WHITE},
            "64": {"bg": (234, 115, 30), "text": WHITE},
            "128": {"bg": (233, 75, 22), "text": WHITE},
            "256": {"bg": (232, 36, 14), "text": WHITE},
            "512": {"bg": (134, 187, 189), "text": WHITE},
            "1024": {"bg": (95, 112, 213), "text": WHITE},
            "2048": {"bg": (55, 36, 237), "text": WHITE},
            "4096": {"bg": (102, 36, 237), "text": WHITE},
            "8192": {"bg": (117, 26, 231), "text": WHITE},
            "16384": {"bg": (132, 17, 225), "text": WHITE},
            "32768": {"bg": (147, 7, 219), "text": WHITE},
        }

        self.update()

    def update(self, tick: bool = False):
        if tick:
            self.move_active_tile()

        # setup board surface
        winsize = self.win.get_size()
        boardsize = int(winsize[1] * 3 / 4)
        self.image = pg.Surface((boardsize, boardsize))
        tilesize = boardsize / 8
        padding = boardsize / 8 / 8
        self.rect = self.image.get_rect()
        self.rect.center = self.win.get_rect().center

        self.image.fill((220, 220, 220))

        # column lines
        for i in range(1, 7):
            pg.draw.line(
                self.image,
                (201, 201, 201),
                (i * (tilesize + padding) + padding * 0.4, padding),
                (i * (tilesize + padding) + padding * 0.4, 7 * (tilesize + padding)),
            )

        # draw tiles
        for rownum, row in enumerate(self.board):
            for colnum, tilevalue in enumerate(row):
                if tilevalue == 0:
                    continue
                else:
                    pos = (
                        colnum * (tilesize + padding) + padding,
                        rownum * (tilesize + padding) + padding,
                    )
                    self.image.blit(self.tile_image(tilevalue, tilesize), pos)

        # draw active tile highlight
        if self.activetile:
            pg.draw.rect(
                self.image,
                (71, 232, 216),
                (
                    self.activetile[1] * (tilesize + padding) + padding,
                    self.activetile[0] * (tilesize + padding) + padding,
                    tilesize,
                    tilesize,
                ),
                max(1, int(tilesize / 30)),
                int(tilesize / 6),
            )

    def move_active_tile(self):
        if self.activetile:
            if (
                self.activetile[0] < 6
                and self.board[self.activetile[0] + 1, self.activetile[1]] == 0
            ):
                # If the tile can move down, move it down
                self.board[self.activetile[0] + 1, self.activetile[1]] = self.board[
                    self.activetile[0], self.activetile[1]
                ]
                self.board[self.activetile[0], self.activetile[1]] = 0
                self.activetile = (self.activetile[0] + 1, self.activetile[1])
                return "moved"
            else:
                self.merge_tiles(self.activetile)
                # Else, spawn a new one at the top
                # If there is a tile already there, lose
                if self.board[0, 3]:
                    global playing
                    playing = False
                    return "death"
                else:
                    self.board[0, 3] = self.nexttile
                    self.activetile = (0, 3)
                    rd.seed()
                    self.nexttile = 2 ** rd.randint(1, 4)
                    return "newtile"
        else:
            if not self.nexttile:
                rd.seed()
                self.nexttile = 2 ** rd.randint(1, 4)
            self.board[0, 3] = self.nexttile
            self.activetile = (0, 3)
            rd.seed()
            self.nexttile = 2 ** rd.randint(1, 4)
            return "newtile"

    def tile_image(self, tilevalue: int, tilesize: int):
        surf = pg.Surface((tilesize, tilesize))
        surf.set_colorkey((254, 254, 254))
        surf.fill((254, 254, 254))

        tilevalue = int(tilevalue)

        rd.seed(tilevalue)

        bg_col, text_col = self.get_tile_colours(tilevalue)

        pg.draw.rect(
            surf,
            bg_col,
            (0, 0, tilesize, tilesize),
            border_radius=int(tilesize / 6),
        )
        # border
        # pg.draw.rect(
        #     surf,
        #     (0, 0, 0),
        #     (0, 0, tilesize, tilesize),
        #     width=max(1, int(tilesize / 30)),
        #     border_radius=int(tilesize / 6),
        # )
        fontsurf = pg.font.SysFont("Arial", int(tilesize / 2)).render(
            str(tilevalue), True, text_col
        )
        fontrect = fontsurf.get_rect()
        fontrect.center = surf.get_rect().center
        surf.blit(fontsurf, fontrect)
        return surf

    def slide(self, direction):
        direction = -1 if direction < 0 else 1
        if (
            self.activetile
            and self.activetile[1] + direction >= 0
            and self.activetile[1] + direction <= 6
        ):
            if self.board[self.activetile[0], self.activetile[1] + direction] == 0:
                self.board[
                    self.activetile[0], self.activetile[1] + direction
                ] = self.board[self.activetile[0], self.activetile[1]]
                self.board[self.activetile[0], self.activetile[1]] = 0
                self.activetile = (self.activetile[0], self.activetile[1] + direction)
                return True

        return False

    def harddrop(self):
        while self.move_active_tile() == "moved":
            pass

    def merge_tiles(self, pos, update_gravity: bool = True):
        merged = 0
        if self.board[pos[0], pos[1]]:
            adjacent = []
            if pos[0] > 0:
                adjacent.append((pos[0] - 1, pos[1]))
            if pos[0] < 6:
                adjacent.append((pos[0] + 1, pos[1]))
            if pos[1] > 0:
                adjacent.append((pos[0], pos[1] - 1))
            if pos[1] < 6:
                adjacent.append((pos[0], pos[1] + 1))

            newvalue = self.board[pos[0], pos[1]]
            for tile in adjacent:
                if self.board[tile[0], tile[1]] == self.board[pos[0], pos[1]]:
                    newvalue *= 2
                    self.board[tile[0], tile[1]] = 0
                    merged += 1

            self.board[pos[0], pos[1]] = newvalue

            if merged:
                print(f"{pos} merged into a {self.board[pos[0], pos[1]]}")
                if update_gravity:
                    self.apply_gravity(ignore_active=False)
                self.merge_tiles(pos)

        return merged

    def apply_gravity(self, ignore_active: bool = True):
        merge_during_gravity = 0
        rows = list(self.board)
        rows.reverse()
        for rownum, row in enumerate(rows):
            for colnum, tilevalue in enumerate(row):
                # flip the rownum because the rows are reversed
                pos = (rownum + 2 * (3 - rownum), colnum)
                if (pos != self.activetile or not ignore_active) and tilevalue != 0:
                    if pos[0] < 6:
                        fell = True
                        while fell:
                            if pos[0] + 1 <= 6:
                                if self.board[pos[0] + 1, pos[1]] == 0:
                                    self.board[pos[0] + 1, pos[1]] = tilevalue
                                    self.board[pos[0], pos[1]] = 0
                                    pos = (pos[0] + 1, pos[1])
                                    fell = True
                                else:
                                    fell = False
                            else:
                                fell = False
                        if pos != (rownum + 2 * (3 - rownum), colnum):
                            print(
                                f"Tile at {(rownum + 2 * (3 - rownum), colnum)} fell to {pos}"
                            )
                            merge_during_gravity = max(
                                merge_during_gravity, int(self.merge_tiles(pos, False))
                            )

        if merge_during_gravity:
            self.apply_gravity(ignore_active)

    def score(self):
        return int(self.board.sum() - self.starting_score)

    def get_tile_colours(self, tilevalue: int):
        return (
            self.tilecolours[str(tilevalue)]["bg"]
            if str(tilevalue) in self.tilecolours.keys()
            else (
                (61, 57, 50)
                if tilevalue > int(max(self.tilecolours.keys()))
                else (rd.randint(100, 255), rd.randint(100, 255), rd.randint(100, 255))
            ),
            self.tilecolours[str(tilevalue)]["text"]
            if str(tilevalue) in self.tilecolours.keys()
            else (255, 255, 255),
        )

    def reset(self):
        self.board = np.zeros((7, 7), dtype=int)
        rd.seed()
        self.board[6] = [2 ** rd.randint(1, 3) for _ in range(7)]
        self.starting_score = self.board.sum()
        self.nexttile = None
        self.activetile = None


class Score(pg.sprite.Sprite):
    def __init__(self, win: pg.Surface, board: Board):
        super().__init__()
        self.win = win
        self.board = board
        self.update()

    def update(self, _=None):
        # create font surface
        self.image = pg.font.SysFont("Arial", int(self.win.get_height() / 25)).render(
            "Score: " + str(self.board.score()), True, (0, 0, 0)
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 10)


class Time(pg.sprite.Sprite):
    def __init__(self, win: pg.Surface):
        super().__init__()
        self.win = win
        self.value = 0
        self.update()

    def update(self, _=None):
        # create font surface
        self.image = pg.font.SysFont("Arial", int(self.win.get_height() / 25)).render(
            "Time: " + str(self.value) + "s", True, (0, 0, 0)
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 45)


class SPS(pg.sprite.Sprite):
    def __init__(self, win: pg.Surface):
        super().__init__()
        self.win = win
        self.value = 0
        self.update()

    def update(self, _=None):
        # create font surface
        self.image = pg.font.SysFont("Arial", int(self.win.get_height() / 25)).render(
            "SPS: " + str(self.value),
            True,
            (0, 0, 0),
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 80)


class APM(pg.sprite.Sprite):
    def __init__(self, win: pg.Surface):
        super().__init__()
        self.win = win
        self.value = 0
        self.update()

    def update(self, _=None):
        # create font surface
        self.image = pg.font.SysFont("Arial", int(self.win.get_height() / 25)).render(
            "APM: " + str(self.value),
            True,
            (0, 0, 0),
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 115)


class DeathText(pg.sprite.Sprite):
    def __init__(self, win: pg.Surface):
        super().__init__()
        self.win = win
        self.active = False
        self.update()

    def update(self, _=None):
        if self.active:
            self.image = pg.font.SysFont(
                "Arial", int(self.win.get_height() / 10)
            ).render("Failed", True, (200, 0, 0))
        else:
            self.image = pg.Surface((0, 0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.win.get_rect().midbottom


class PauseText(pg.sprite.Sprite):
    def __init__(self, win: pg.Surface):
        super().__init__()
        self.win = win
        self.active = False
        self.update()

    def update(self, _=None):
        if self.active:
            self.image = pg.font.SysFont(
                "Arial", int(self.win.get_height() / 10)
            ).render("Paused", True, (150, 150, 150))
        else:
            self.image = pg.Surface((0, 0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.win.get_rect().midbottom


def end(q: bool = True):
    with open("performance_history.json", "r") as f:
        data = json.load(f)
    data[dt.now().strftime("%y/%m/%d %H:%M.%S")] = performance
    with open("performance_history.json", "w") as f:
        json.dump(data, f, indent=2)
    if q:
        pg.quit()
        quit()


def reset():
    global BOARD, igt, actions, performance, playing, paused, timesincetick
    end(False)
    BOARD.reset()
    igt = 0
    actions = 0
    performance = {}
    playing = True
    paused = False
    timesincetick = 0


clock = pg.time.Clock()

paused = False

elements = pg.sprite.Group()
BOARD = Board(WIN)
elements.add(BOARD)
elements.add(Score(WIN, BOARD))
deathtext = DeathText(WIN)
pausetext = PauseText(WIN)
elements.add(deathtext, pausetext)

timetext = Time(WIN)
spstext = SPS(WIN)
apmtext = APM(WIN)

elements.add(timetext, spstext, apmtext)

tickinterval = 700

timesincetick = 0
igt = 0
actions = 0

performance = {}

speed_keys = {pg.K_q: -3, pg.K_w: -2, pg.K_e: -1, pg.K_i: 1, pg.K_o: 2, pg.K_p: 3}

playing = True
while True:
    delta = clock.tick(60)
    winsize = WIN.get_size()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            end()
        elif event.type == pg.KEYDOWN:
            if playing and not paused:
                actions += 1
                if event.key == pg.K_RIGHT:
                    BOARD.slide(1)
                elif event.key == pg.K_LEFT:
                    BOARD.slide(-1)
                elif event.key == pg.K_SPACE:
                    BOARD.harddrop()
                    timesincetick = 0
                # Speed keys
                elif event.key in speed_keys.keys():
                    success = True
                    for i in range(abs(speed_keys[event.key])):
                        success = min(success, BOARD.slide(speed_keys[event.key]))
                    if success:
                        BOARD.harddrop()

                else:
                    actions -= 1

            if event.key == pg.K_ESCAPE:
                paused = not paused
            if event.key == pg.K_r and (paused or not playing):
                reset()

    if playing and not paused:
        igt += delta
        timesincetick += delta

        score = BOARD.score()
        sps = score / (igt / 1000)
        apm = actions / (igt / 60000)

        deathtext.active = False
        pausetext.active = False
        timetext.value = round(igt / 1000)
        spstext.value = round(sps, 1)
        apmtext.value = round(apm, 1)

        if not "raw" in performance.keys():
            performance["raw"] = {}
        performance["raw"][str(igt)] = {
            "time": igt,
            "sps": sps,
            "score": score,
            "aps": apm / 60,
            "apm": apm,
        }
        if timesincetick >= tickinterval:
            tick = True
            timesincetick = 0
        else:
            tick = False
    elif not playing:
        deathtext.active = True
        pausetext.active = False
    else:
        deathtext.active = False
        pausetext.active = True

    WIN.fill((255, 255, 255))
    # draw next tile prompt ((1/8 - 1/10) / 2 = 1/80)
    if BOARD.nexttile:
        next_tile_size = WIN.get_height() / 10
        WIN.blit(
            BOARD.tile_image(BOARD.nexttile, next_tile_size),
            (WIN.get_width() / 2 - next_tile_size / 2, WIN.get_height() / 80),
        )

    elements.update(tick)
    elements.draw(WIN)

    pg.display.update()
