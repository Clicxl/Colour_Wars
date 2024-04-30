import pygame
from pygame.constants import *
from sys import exit
from scripts.Settings import *
from scripts.States import *


class Game:
    def __init__(self):

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("Color Wars")
        self.running = True
        self.font = pygame.font.Font(FONT, SCALE * TILESIZE)
        self.states = []

        # State Classes
        self.splash_screen = SplashScreen(self)

        self.states.append(self.splash_screen)

        play("assets/Audio/song.mp3", vol=VOLUME, fade=2, loop=1)

    def user_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                exit()

            if event.type == pygame.KEYDOWN:
                # KEYDOWN

                # Space & Escape
                if event.key == K_ESCAPE:
                    INPUTS["escape"] = True
                    self.running = False
                elif event.key == K_SPACE:
                    INPUTS["space"] = True
                elif event.key == K_r:
                    INPUTS['r'] = True

            if event.type == pygame.KEYUP:
                # KEYUP
                # Space & Escape
                if event.key == K_ESCAPE:
                    INPUTS["escape"] = False
                elif event.key == K_SPACE:
                    INPUTS["space"] = False
                elif event.key == K_r:
                    INPUTS['r'] = False

            # MOOUSEDOWN

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    INPUTS["left_click"] = True

            # Mouse Button
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    INPUTS["left_click"] = False

    def reset_input(self):
        for key in INPUTS:
            INPUTS[key] = False

    # Utils
    def render_font(
        self,
        text: str,
        color: tuple,
        pos: pygame.Vector2,
        font: pygame.font.Font,
        centerlized: bool = True,
    ):

        surf = font.render(str(text), False, color)
        rect = surf.get_rect(center=pos) if centerlized else surf.get_rect(topleft=pos)
        self.screen.blit(surf, rect)

    def custom_crosshair(self):
        crosshari = pygame.transform.scale(
            pygame.image.load(
                "assets/Images/game_assets/Crosshair.png"
            ).convert_alpha(),
            (TILESIZE * SCALE, TILESIZE * SCALE),
        )
        crosshari.set_alpha(150)
        crosshair_rect = crosshari.get_frect(center=pygame.mouse.get_pos())
        self.screen.blit(crosshari, crosshair_rect.center)

    def loop(self):
        while self.running:
            self.dt = self.clock.tick() / 1000
            self.user_input()
            self.screen.fill(COLORS["black"])

            self.states[-1].update(self.dt)
            self.states[-1].draw(self.screen)

            self.custom_crosshair()
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.loop()
