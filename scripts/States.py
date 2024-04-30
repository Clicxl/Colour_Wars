import pygame
from scripts.Settings import *
from scripts.Camera import *
from scripts.Board import *
from scripts.Objects import *
from scripts.Utils import play


class State:
    def __init__(self, game):
        self.game = game

    def enter_state(self):
        if len(self.game.states) > 1:
            self.prev_state = self.game.states[-1]
        self.game.states.append(self)

    def exit_state(self):
        self.game.states.pop()

    def debugger(self, defbug_list):
        for index, name in enumerate(defbug_list):
            self.game.render_font(
                str(name), COLORS["white"], vec(10, 35 * index), self.game.font, False
            )

    def draw(self, screen):
        pass

    def update(self, dt):
        pass


class SplashScreen(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.load_images()
        self.update_sprites = pygame.sprite.Group()
        self.draw_sprites = pygame.sprite.Group()

        self.logo = Logo([self.update_sprites, self.draw_sprites])

    def load_images(self):

        self.bg = pygame.image.load("assets/Images/Background.png").convert_alpha()
        self.bg_rect = self.bg.get_frect(topleft=vec(0, 0))

    def draw(self, screen):
        screen.blit(self.bg, self.bg_rect)
        self.draw_sprites.draw(screen)
        self.game.render_font(
            "Press Space To Start",
            COLORS["white"],
            vec(WIDTH / 2, 2 * HEIGHT / 3),
            self.game.font,
        )

    def update(self, dt):
        self.logo.update(dt)

        if INPUTS["space"] == True:
            Scene(self.game).enter_state()
            self.game.reset_input()


class Scene(State):
    def __init__(self, game):
        super().__init__(game)

        self.camera = Camera(self)
        self.update_sprites = pygame.sprite.Group()
        self.draw_sprites = pygame.sprite.Group()
        self.game = game

        self.board = Board([self.update_sprites, self.draw_sprites], game)

    def draw(self, screen):
        self.camera.draw(screen, self.draw_sprites)
        self.debugger([str(f"FPS: {self.game.clock.get_fps():.2f}")])

    def update(self, dt):

        self.update_sprites.update(dt)
        self.camera.update(dt)
        self.board.update(dt)
        if self.board.winner == "red":
            EndScreen(self.game, "Red", COLORS["red"]).enter_state()
        elif self.board.winner == "blue":
            EndScreen(self.game, "Blue", COLORS["blue"]).enter_state()


class EndScreen(State):
    def __init__(self, game, winner, win_col):
        super().__init__(game)

        self.camera = Camera(self)
        self.update_sprites = pygame.sprite.Group()
        self.draw_sprites = pygame.sprite.Group()
        self.winner = winner
        self.win_col = win_col
        play("assets/Audio/End.wav", vol=VOLUME * 5, fade=1, loop=0)

    def draw(self, screen):
        screen.fill(self.win_col)
        self.camera.draw(screen, self.draw_sprites)
        self.game.render_font(
            f"{self.winner} Won the Game",
            COLORS["white"],
            pygame.Vector2(WIDTH / 2, HEIGHT / 2),
            self.game.font,
        )
        self.debugger([str(f"FPS: {self.game.clock.get_fps():.2f}")])

        self.game.render_font(
            "Press 'R' to Restart",
            COLORS["yellow"],
            vec(WIDTH / 2, 2 * HEIGHT / 3),
            self.game.font,
        )
        self.game.render_font(
            "Game By Clicxl",
            COLORS["white"],
            vec(WIDTH / 2, 3 * HEIGHT / 4),
            self.game.font,
        )

    def update(self, dt):
        self.update_sprites.update(dt)
        self.camera.update(dt)
        if INPUTS["r"]:
            Scene(self.game).enter_state()
            self.game.reset_input()
