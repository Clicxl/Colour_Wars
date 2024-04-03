import pygame
from scripts.Settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, row, col, surfs):
        super().__init__(groups)
        self.col = col
        self.row = row
        self.value = 00
        self.surfs = surfs
        self.clicked = False

        self.image = self.surfs[str(self.value)]
        self.rect = self.image.get_frect()

    def get_pos(self):
        return [self.col, self.row]

    def draw(self, screen):
        pass

    def update(self, dt):
        try:
            self.image = self.surfs[str(self.value)]
        except KeyError:
            self.image = self.surfs['0']

    def __repr__(self):
        return f"Tile {self.col}x{self.row}"

    def get_clicked(self,):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse) and INPUTS['left_click'] and self.clicked == False:
            return True

        elif INPUTS['left_click'] == False:
            return False
