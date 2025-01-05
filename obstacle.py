import pygame
from random import randint
from constants import ground_y

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            self.frames = [
                pygame.image.load('graphics/fly/fly1.png').convert_alpha(),
                pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            ]
            y_pos = ground_y - 90
        else:
            self.frames = [
                pygame.image.load('graphics/slime/slime1.png').convert_alpha(),
                pygame.image.load('graphics/slime/slime2.png').convert_alpha()
            ]
            y_pos = ground_y
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        if self.rect.x <= -100:
            self.kill()
