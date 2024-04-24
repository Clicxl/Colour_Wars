import pygame, csv
from scripts.Settings import *


class Camera(pygame.sprite.Group):
    def __init__(self, scene):
        self.offset = vec()
        self.visible_window = pygame.FRect(0, 0, WIDTH, HEIGHT)
        self.delay = 2

    def update(self, dt):
        pass

    def draw(self, screen, group):
        screen.blit(
            pygame.image.load("assets/Images/Background.png").convert_alpha(), (0, 0)
        )
        group.draw(screen)
