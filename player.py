import pygame
from constants import ground_y

class Player(pygame.sprite.Sprite):
    def __init__(self, ground_y):
        super().__init__()
        self.player_walk = [
            pygame.image.load('graphics/player/knight_walk_1.png').convert_alpha(),
            pygame.image.load('graphics/player/knight_walk_2.png').convert_alpha()
        ]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, ground_y))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('sounds/jump.wav')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= ground_y:
            self.gravity = -15
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y

    def animation_state(self):
        if self.rect.bottom < ground_y:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
