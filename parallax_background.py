import pygame

class ParallaxBackground:
    def __init__(self):
        self.bg_images = []
        for i in range(1, 6):
            bg_image = pygame.image.load(f'graphics/plx-{i}.png').convert_alpha()
            self.bg_images.append(bg_image)
        self.bg_width = self.bg_images[0].get_width()
        self.scroll = 0
        
    def draw(self, screen):
        for x in range(5):
            speed = 1
            for i in self.bg_images:
                screen.blit(i, ((x * self.bg_width) - self.scroll * speed, 0))
                speed += 0.2
        self.scroll += 2
        if self.scroll * 0.5 >= self.bg_width:
            self.scroll = 0