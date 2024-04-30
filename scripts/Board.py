import pygame
from scripts.Utils import Image, play
from scripts.Objects import Tile
from scripts.Settings import *


class Board:
    def __init__(self, groups, game):
        self.groups = groups
        self.load_surf("assets/Images/tiles")
        self.board_data = self.create_board()
        self.player = "red"
        self.red_first = False
        self.blue_first = False
        self.winner = None
        self.game = game

    def create_board(self, size=5):
        self.size = size
        self.board = []
        for i in range(size):
            self.board.append([])
            for j in range(size):
                self.board[i].append(Tile(self.groups, j, i, self.surfs))
                self.board[i][j].rect.topleft = (
                    WIDTH / 3 + (SCALE * (TILESIZE * SCALE) + PADDING) * j,
                    HEIGHT / 3 + (SCALE * (TILESIZE * SCALE) + PADDING) * i,
                )
        return self.board

    def load_surf(self, path):
        image = Image()
        self.surfs = image.get_images(path, 2)

    def click_event(self, tile):
        if tile.get_clicked():
            if self.player == "red" and (
                (self.red_first == False and tile.value == 0) or tile.value > 0
            ):
                tile.value += 1
                self.player = "blue"
                self.reset_input()
                self.red_first = True
                play("assets/Audio/click.wav", vol=VOLUME, fade=0, loop=0)

            elif self.player == "blue" and (
                (self.blue_first == False and tile.value == 0) or tile.value < 0
            ):
                tile.value -= 1
                self.player = "red"
                self.reset_input()
                self.blue_first = True
                play("assets/Audio/click.wav", vol=VOLUME, fade=0, loop=0)

    def tile_split(self, tile, dt):
        col, row = tile.get_pos()
        # Red
        if tile.value >= 4:
            play("assets/Audio/split.wav", fade=0, vol=VOLUME, loop=0)

            # Colums
            if 0 < col < self.size - 1:
                if self.board[col + 1][row].value < 0:
                    self.board[col + 1][row].value = (
                        abs(self.board[col + 1][row].value) + 1
                    )
                else:
                    self.board[col + 1][row].value += 1

                if self.board[col - 1][row].value < 0:
                    self.board[col - 1][row].value = (
                        abs(self.board[col - 1][row].value) + 1
                    )
                else:
                    self.board[col - 1][row].value += 1

            # Edges | Columns
            elif col == 0:
                if self.board[col + 1][row].value >= 0:
                    self.board[col + 1][row].value += 1
                elif self.board[col + 1][row].value < 0:
                    self.board[col + 1][row].value = (
                        abs(self.board[col + 1][row].value) + 1
                    )

            elif col == self.size - 1:
                if self.board[col - 1][row].value >= 0:
                    self.board[col - 1][row].value += 1
                elif self.board[col - 1][row].value < 0:
                    self.board[col - 1][row].value = (
                        abs(self.board[col - 1][row].value) + 1
                    )

            # Rows
            if 0 < row < self.size - 1:
                if self.board[col][row + 1].value < 0:
                    self.board[col][row + 1].value = (
                        abs(self.board[col][row + 1].value) + 1
                    )
                else:
                    self.board[col][row + 1].value += 1

                if self.board[col][row - 1].value < 0:
                    self.board[col][row - 1].value = (
                        abs(self.board[col][row - 1].value) + 1
                    )
                else:
                    self.board[col][row - 1].value += 1

            # Edges | Rows
            elif row == 0:
                if self.board[col][row + 1].value >= 0:
                    self.board[col][row + 1].value += 1
                elif self.board[col][row + 1].value < 0:
                    self.board[col][row + 1].value = (
                        abs(self.board[col][row + 1].value) + 1
                    )

            elif row == self.size - 1:
                if self.board[col][row - 1].value >= 0:
                    self.board[col][row - 1].value += 1
                elif self.board[col][row - 1].value < 0:
                    self.board[col][row - 1].value = (
                        abs(self.board[col][row - 1].value) + 1
                    )
            tile.value = 0

        # Blue
        if tile.value == -4:
            play("assets/Audio/split.wav", fade=0, vol=VOLUME, loop=0)

            # Colums
            if 0 < col < self.size - 1:
                if self.board[col + 1][row].value > 0:
                    self.board[col + 1][row].value = (
                        -abs(self.board[col + 1][row].value) - 1
                    )
                else:
                    self.board[col + 1][row].value -= 1

                if self.board[col - 1][row].value > 0:
                    self.board[col - 1][row].value = (
                        -abs(self.board[col - 1][row].value) - 1
                    )
                else:
                    self.board[col - 1][row].value -= 1

            # Edges | Columns
            elif col == 0:
                if self.board[col + 1][row].value <= 0:
                    self.board[col + 1][row].value -= 1
                elif self.board[col + 1][row].value > 0:
                    self.board[col + 1][row].value = (
                        -abs(self.board[col + 1][row].value) - 1
                    )

            elif col == self.size - 1:
                if self.board[col - 1][row].value <= 0:
                    self.board[col - 1][row].value -= 1
                elif self.board[col - 1][row].value > 0:
                    self.board[col - 1][row].value = (
                        -abs(self.board[col - 1][row].value) - 1
                    )

            # Rows
            if 0 < row < self.size - 1:
                if self.board[col][row + 1].value > 0:
                    self.board[col][row + 1].value = (
                        -abs(self.board[col][row + 1].value) - 1
                    )
                else:
                    self.board[col][row + 1].value -= 1

                if self.board[col][row - 1].value > 0:
                    self.board[col][row - 1].value = (
                        -abs(self.board[col][row - 1].value) - 1
                    )
                else:
                    self.board[col][row - 1].value -= 1

            # Edges | Rows
            elif row == 0:
                if self.board[col][row + 1].value <= 0:
                    self.board[col][row + 1].value -= 1
                elif self.board[col][row + 1].value > 0:
                    self.board[col][row + 1].value = (
                        -abs(self.board[col][row + 1].value) - 1
                    )

            elif row == self.size - 1:
                if self.board[col][row - 1].value <= 0:
                    self.board[col][row - 1].value -= 1
                elif self.board[col][row - 1].value > 0:
                    self.board[col][row - 1].value = (
                        -abs(self.board[col][row - 1].value) - 1
                    )

            tile.value = 0

    def win(self):
        red = 0
        blue = 0

        for col in self.board:
            for tile in col:
                if self.blue_first and self.red_first == True:
                    if tile.value > 0:
                        red += 1
                    elif tile.value < 0:
                        blue += 1

        if red > 0 and blue == 0:
            self.winner = "red"
        elif blue > 0 and red == 0:
            self.winner = "blue"

    def reset_input(self):
        for key in INPUTS:
            INPUTS[key] = False

    def update(self, dt):
        for _ in self.board:
            for tile in _:
                self.click_event(tile)
                self.tile_split(tile, dt)

        self.win()
