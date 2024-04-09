import pygame
from scripts.Image import Image
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
            if self.player == "red" and (self.red_first == False or tile.value > 0):
                tile.value += 1
                self.player = "blue"
                self.reset_input()
                self.red_first = True

            elif self.player == "blue" and (self.blue_first == False or tile.value < 0):
                tile.value -= 1
                self.player = "red"
                self.reset_input()
                self.blue_first = True

    def tile_split(self, tile):
        col, row = tile.get_pos()

        if tile.value >= 4:
            self.reset_input()
            tile.value = 0
            if self.board[col - 1][row].value < 0 or self.board[col + 1][row].value < 0:
                self.board[col + 1][row].value = abs(self.board[col + 1][row].value) + 1
                self.board[col - 1][row].value = abs(self.board[col - 1][row].value) + 1
            else:
                self.board[col + 1][row].value += 1
                self.board[col - 1][row].value += 1

            if self.board[col][row + 1].value < 0 or self.board[col][row - 1].value < 0:
                self.board[col][row + 1].value = abs(self.board[col][row + 1].value) + 1
                self.board[col][row - 1].value = abs(self.board[col][row - 1].value) + 1
            else:
                self.board[col][row + 1].value += 1
                self.board[col][row - 1].value += 1

        elif tile.value <= -4:
            self.reset_input()
            tile.value = 0

            if self.board[col - 1][row].value > 0 or self.board[col + 1][row].value > 0:
                self.board[col + 1][row].value = (
                    self.board[col + 1][row].value * -1
                ) - 1
                self.board[col - 1][row].value = (
                    self.board[col - 1][row].value * -1
                ) - 1
            else:
                self.board[col + 1][row].value -= 1
                self.board[col - 1][row].value -= 1

            if self.board[col][row - 1].value > 0 or self.board[col][row + 1].value > 0:
                self.board[col][row + 1].value = (
                    self.board[col][row + 1].value * -1
                ) - 1
                self.board[col][row - 1].value = (
                    self.board[col][row - 1].value * -1
                ) - 1
            else:
                self.board[col][row + 1].value -= 1
                self.board[col][row - 1].value -= 1

    def win(self):
        values = [tile.value for row in self.board for tile in row]
        red = 0
        blue = 0

        if self.blue_first and self.red_first == True:
            for x in values:
                if x > 0:
                    red += 1
                elif x < 0:
                    blue += 1

        if red > 0 and blue == 0:
            pass
        elif blue > 0 and red == 0:
            pass

    def reset_input(self):
        for key in INPUTS:
            INPUTS[key] = False

    def update(self, dt):
        for _ in self.board:
            for tile in _:
                self.click_event(tile)
                self.tile_split(tile)
                self.win()
