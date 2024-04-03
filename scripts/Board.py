import pygame
from scripts.Image import Image
from scripts.Objects import Tile
from scripts.Settings import *


class Board:
    def __init__(self, groups):
        self.groups = groups
        self.load_surf('assets/Images/tiles')
        self.board_data = self.create_board()
        self.player = 'red'
        self.red_first = False
        self.blue_first = False

    def create_board(self, size=5):
        self.board = []
        for i in range(size):
            self.board.append([])
            for j in range(size):
                self.board[i].append(Tile(self.groups, j, i, self.surfs))
                self.board[i][j].rect.topleft = (
                    WIDTH/3 + (SCALE*(TILESIZE*SCALE)+PADDING)*j, HEIGHT/3 + (SCALE*(TILESIZE*SCALE)+PADDING)*i)
        return self.board

    def load_surf(self, path):
        image = Image()
        self.surfs = image.get_images(path, 2)

    def click_event(self):
        for row in self.board:
            for tile in row:
                if tile.get_clicked():
                    if self.player == 'red' and (self.red_first == False or tile.value > 0):
                        tile.value += 1
                        self.player = 'blue'
                        self.reset_input()
                        self.red_first = True

                    elif self.player == 'blue' and (self.blue_first == False or tile.value < 0):
                        tile.value -= 1
                        self.player = 'red'
                        self.reset_input()
                        self.blur_first = True

    def tile_split(self):
        for i in range(len(self.board)):
            for j in range(i):
                if self.board[i][j].value > 4:
                    self.reset_input()
                    self.board[i][j+1].value += 1
                    self.board[i][j-1].value += 1
                    self.board[i+1][j].value += 1
                    self.board[i-1][j].value += 1
                    self.board[i][j].value = 0

                if self.board[i][j].value < -4:
                    self.reset_input()
                    self.board[i][j+1].value -= 1
                    self.board[i][j-1].value -= 1
                    self.board[i+1][j].value -= 1
                    self.board[i-1][j].value -= 1
                    self.board[i][j].value = 0

    def reset_input(self):
        for key in INPUTS:
            INPUTS[key] = False

    def update(self, dt):
        self.click_event()
        self.tile_split()