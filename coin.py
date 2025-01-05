import pygame
from random import randint

class Coin(pygame.sprite.Sprite):
    def __init__(self, ground_y):
        super().__init__()

        sprite_sheet = pygame.image.load("graphics/coin/coin.png").convert_alpha()
        sprite_width = sprite_sheet.get_width() // 12
        sprite_height = sprite_sheet.get_height()

        self.frames = []
        for col in range(12):
            frame = sprite_sheet.subsurface((col * sprite_width, 0, sprite_width, sprite_height))
            frame = pygame.transform.scale(frame, (int(sprite_width * 1.5), int(sprite_height * 1.5)))
            self.frames.append(frame)

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), ground_y - 100))

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