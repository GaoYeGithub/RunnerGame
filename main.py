import pygame
from sys import exit
import importlib.resources as resources
from random import randint, choice
import math
import asyncio
import sys
from pathlib import Path

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_Y = SCREEN_HEIGHT - 63
TITLE_COLOR = (255, 223, 0)
TEXT_COLOR = (255, 255, 255)
SHADOW_COLOR = (20, 20, 20)

class Player(pygame.sprite.Sprite):
    def __init__(self, assets_path):
        super().__init__()
        player_walk_1 = pygame.image.load(assets_path / 'graphics/Player/knight_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load(assets_path / 'graphics/Player/knight_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load(assets_path / 'graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, ground_y))
        self.gravity = 0
        self.animation_speed = 5

        self.jump_sound = pygame.mixer.Sound(assets_path / 'sounds/jump.wav')
        self.jump_sound.set_volume(0.5)
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -10
            self.jump_sound.play()

    def apply_gravity(self, dt):
        self.gravity += 30 * dt
        self.rect.y += self.gravity * dt * 60
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y

    def animation_state(self, dt):
        if self.rect.bottom < 300: 
            self.image = self.player_jump
        else:
            self.player_index += self.animation_speed * dt
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self, dt):
        self.player_input()
        self.apply_gravity(dt)
        self.animation_state(dt)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, assets_path):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load(assets_path / 'graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load(assets_path / 'graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = ground_y - 90
        else:
            slime_1 = pygame.image.load(assets_path / 'graphics/slime/slime1.png').convert_alpha()
            slime_2 = pygame.image.load(assets_path / 'graphics/slime/slime2.png').convert_alpha()
            self.frames = [slime_1, slime_2]
            y_pos = ground_y
    
        self.animation_index = 0
        self.animation_speed = 5
        self.movement_speed = 360
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900,1100), y_pos))

    def animation_state(self, dt):
        self.animation_index += self.animation_speed * dt
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self, dt):
        self.animation_state(dt)
        self.rect.x -= self.movement_speed * dt
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100: 
            self.kill()

class ParallaxBackground:
    def __init__(self, assets_path):
        self.bg_images = []
        for i in range(1, 6):
            bg_image = pygame.image.load(assets_path / f'graphics/plx-{i}.png').convert_alpha()
            self.bg_images.append(bg_image)
        self.bg_width = self.bg_images[0].get_width()
        self.scroll = 0
        self.scroll_speed = 12
        
    def draw(self, screen, dt):
        for x in range(5):
            speed = 1
            for i in self.bg_images:
                screen.blit(i, ((x * self.bg_width) - self.scroll * speed, 0))
                speed += 0.2
        self.scroll += self.scroll_speed * dt
        if self.scroll * 0.5 >= self.bg_width:
            self.scroll = 0

class Ground:
    def __init__(self, assets_path):
        self.ground_image = pygame.image.load(assets_path / 'graphics/ground.png').convert_alpha()
        self.ground_width = self.ground_image.get_width()
        self.ground_height = self.ground_image.get_height()
        self.scroll = 0
        self.scroll_speed = 150
        
    def draw(self, screen, dt):
        for x in range(15):
            screen.blit(self.ground_image, 
                       ((x * self.ground_width) - self.scroll * 2.5, 
                        400 - self.ground_height))
        self.scroll += self.scroll_speed * dt
        if self.scroll * 2.5 >= self.ground_width:
            self.scroll = 0

class Coin(pygame.sprite.Sprite):
    def __init__(self, ground_y, assets_path):
        super().__init__()

        sprite_sheet = pygame.image.load(assets_path / "graphics/coin/coin.png").convert_alpha()
        sprite_width = sprite_sheet.get_width() // 12
        sprite_height = sprite_sheet.get_height()

        self.frames = []
        for col in range(12):
            frame = sprite_sheet.subsurface((col * sprite_width, 0, sprite_width, sprite_height))
            frame = pygame.transform.scale(frame, (int(sprite_width * 1.5), int(sprite_height * 1.5)))
            self.frames.append(frame)

        self.animation_index = 0
        self.animation_speed = 5
        self.movement_speed = 360
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), ground_y - 100))

    def animation_state(self, dt):
        self.animation_index += self.animation_speed * dt
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self, dt):
        self.animation_state(dt)
        self.rect.x -= self.movement_speed * dt
        if self.rect.x <= -100:
            self.kill()


def display_score():

    score_surf = test_font.render(f'Score: {score}', False, (255, 255, 255))
    score_rect = score_surf.get_rect(center=(400, 50))
    shadow_surf = test_font.render(f'Score: {score}', False, (20, 20, 20))
    shadow_rect = shadow_surf.get_rect(center=(402, 52))
    
    screen.blit(shadow_surf, shadow_rect)
    screen.blit(score_surf, score_rect)
    
def update_score():
    global score
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score = current_time + coin_points


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True

class MenuAnimation:
    def __init__(self):
        self.time = 0
        self.hover_amplitude = 20
        self.rotation = 0
        self.rotation_speed = 60
        
    def update(self, dt):
        self.time += 3 * dt
        self.rotation += self.rotation_speed * dt
        if self.rotation >= 360:
            self.rotation = 0
            
    def get_pos_offset(self):
        return math.sin(self.time) * self.hover_amplitude

def check_coin_collision():
    global coin_points
    collected_coins = pygame.sprite.spritecollide(player.sprite, coin_group, True)
    if collected_coins:
        coin_points += len(collected_coins) * 10


async def main():
    global ground_y, score, coin_points

    if getattr(sys, 'frozen', False):
        assets_path = Path(sys._MEIPASS)
    else:
        assets_path = Path(__file__).parent

    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 400
    ground_y = SCREEN_HEIGHT - 63

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Runner')
    clock = pygame.time.Clock()

    TITLE_COLOR = (255, 223, 0)
    TEXT_COLOR = (255, 255, 255)
    SHADOW_COLOR = (20, 20, 20)

    test_font = pygame.font.Font(assets_path / 'fonts/PixelOperator8.ttf', 50)
    game_active = False
    start_time = 0
    score = 0
    coin_points = 0

    bg_music = pygame.mixer.Sound(assets_path / 'sounds/music.wav')
    bg_music.play(loops=-1)

    player = pygame.sprite.GroupSingle()
    player.add(Player(assets_path))
    obstacle_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()

    coin_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(coin_timer, 2000)

    parallax_bg = ParallaxBackground(assets_path)
    ground = Ground(assets_path)

    player_stand = pygame.image.load(assets_path / 'graphics/Player/knight_stand.png').convert_alpha()
    player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
    player_stand_rect = player_stand.get_rect(center=(400, 200))
    menu_animation = MenuAnimation()

    game_name = test_font.render('Pixel Runner', False, TITLE_COLOR)
    game_name_rect = game_name.get_rect(center=(400, 80))
    game_name_shadow = test_font.render('Pixel Runner', False, SHADOW_COLOR)
    game_name_shadow_rect = game_name_shadow.get_rect(center=(402, 82))

    game_message = test_font.render('Press space to run', False, TEXT_COLOR)
    game_message_rect = game_message.get_rect(center=(400, 330))
    game_message_shadow = test_font.render('Press space to run', False, SHADOW_COLOR)
    game_message_shadow_rect = game_message_shadow.get_rect(center=(402, 332))

    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 1500)

    previous_time = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()
        dt = (current_time - previous_time) / 1000.0
        previous_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if game_active:
                if event.type == obstacle_timer:
                    obstacle_group.add(Obstacle(choice(['fly', 'slime', 'slime', 'slime']), assets_path))
                if event.type == coin_timer:
                    coin_group.add(Coin(ground_y, assets_path))
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)
                    score = 0
                    coin_points = 0
                    obstacle_group.empty()
                    coin_group.empty()

        if game_active:
            parallax_bg.draw(screen, dt)
            ground.draw(screen, dt)

            current_time = int(pygame.time.get_ticks() / 1000) - start_time
            score = current_time + coin_points

            score_surf = test_font.render(f'Score: {score}', False, TEXT_COLOR)
            score_rect = score_surf.get_rect(center=(400, 50))
            shadow_surf = test_font.render(f'Score: {score}', False, SHADOW_COLOR)
            shadow_rect = shadow_surf.get_rect(center=(402, 52))
            screen.blit(shadow_surf, shadow_rect)
            screen.blit(score_surf, score_rect)

            if pygame.sprite.spritecollide(player.sprite, coin_group, True):
                coin_points += 10

            player.draw(screen)
            player.update(dt)

            obstacle_group.draw(screen)
            obstacle_group.update(dt)

            coin_group.draw(screen)
            coin_group.update(dt)

            if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
                obstacle_group.empty()
                game_active = False

        else:
            for i in range(SCREEN_HEIGHT):
                color = (94 - i // 8, 129 - i // 8, 162 - i // 8)
                pygame.draw.line(screen, color, (0, i), (SCREEN_WIDTH, i))

            menu_animation.update(dt)
            rotated_player = pygame.transform.rotate(player_stand, menu_animation.rotation * 0.1)
            player_stand_rect.centery = 200 + menu_animation.get_pos_offset()
            screen.blit(rotated_player, rotated_player.get_rect(center=player_stand_rect.center))

            if score == 0:
                screen.blit(game_message_shadow, game_message_shadow_rect)
                screen.blit(game_message, game_message_rect)
            else:
                score_message = test_font.render(f'Your score: {score}', False, TEXT_COLOR)
                score_message_rect = score_message.get_rect(center=(400, 330))
                score_shadow = test_font.render(f'Your score: {score}', False, SHADOW_COLOR)
                score_shadow_rect = score_shadow.get_rect(center=(402, 332))
                screen.blit(score_shadow, score_shadow_rect)
                screen.blit(score_message, score_message_rect)

            screen.blit(game_name_shadow, game_name_shadow_rect)
            screen.blit(game_name, game_name_rect)

        pygame.display.update()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())