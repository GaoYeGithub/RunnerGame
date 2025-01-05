import math
from player import Player
from parallax_background import ParallaxBackground
from ground import Ground
from menu_animation import MenuAnimation
import pygame
from constants import ground_y

player = pygame.sprite.GroupSingle()
player.add(Player(ground_y))

obstacle_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

parallax_bg = ParallaxBackground()
ground = Ground()
menu_animation = MenuAnimation()

class MenuAnimation:
    def __init__(self):
        self.time = 0
        self.hover_amplitude = 20
        self.rotation = 0
        
    def update(self):
        self.time += 0.05
        self.rotation += 1
        if self.rotation >= 360:
            self.rotation = 0
            
    def get_pos_offset(self):
        return math.sin(self.time) * self.hover_amplitude
    
    def draw(self, screen, font, bottom_position, score):
        rotated_player = pygame.transform.rotate(player_stand, self.rotation * 0.1)
        player_stand_rect.centery = 200 + self.get_pos_offset()
        screen.blit(rotated_player, rotated_player.get_rect(center=player_stand_rect.center))
        
        if score == 0:
            screen.blit(game_message_shadow, game_message_shadow_rect)
            screen.blit(game_message, game_message_rect)
        else:
            score_message = font.render(f'Your score: {score}', False, TEXT_COLOR)
            score_message_rect = score_message.get_rect(center=(400, 330))
            score_shadow = font.render(f'Your score: {score}', False, SHADOW_COLOR)
            score_shadow_rect = score_shadow.get_rect(center=(402, 332))

            screen.blit(score_shadow, score_shadow_rect)
            screen.blit(score_message, score_message_rect)

        screen.blit(game_name_shadow, game_name_shadow_rect)
        screen.blit(game_name, game_name_rect)
