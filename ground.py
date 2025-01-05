import pygame
from constants import SCREEN_HEIGHT

class Ground:
    def __init__(self):
        self.ground_image = pygame.image.load('graphics/ground.png').convert_alpha()
        self.ground_width = self.ground_image.get_width()
        self.ground_height = self.ground_image.get_height()
        self.scroll = 0
        
    def draw(self, screen):
        for x in range(15):
            screen.blit(self.ground_image, 
                       ((x * self.ground_width) - self.scroll * 2.5, 
                        SCREEN_HEIGHT - self.ground_height))
        self.scroll += 2
        if self.scroll * 2.5 >= self.ground_width:
            self.scroll = 0