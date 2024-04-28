import pygame
from bullet import Bullet

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

class Player(pygame.sprite.Sprite):
    def __init__(self,character):
        super().__init__()
        self.player_frames = []
        self.character = character
        self.update_character()
        if character == 0:
            for i in range(1, 11):
                self.player_frames.append(pygame.image.load('graphics/player/naga_1/{}.png'.format(i)).convert_alpha())
        elif character == 1:
            for i in range(1, 11):
                self.player_frames.append(pygame.image.load('graphics/player/naga_2/{}.png'.format(i)).convert_alpha())
        else:
            for i in range(1, 11):
                self.player_frames.append(pygame.image.load('graphics/player/naga_3/{}.png'.format(i)).convert_alpha())
        self.player_frames = [pygame.transform.smoothscale(image, (110, 75)) for image in self.player_frames]
        self.player_frame_index = 0
        
        self.image = self.player_frames[self.player_frame_index]
        self.rect = self.image.get_rect(midbottom = (200, (SCREEN_HEIGHT/2)))

        self.bullet_active = False
        self.active_time = 0

        self.ready = True
        self.bullet_time = 0
        self.bullet_cooldown = 600
        self.indicator_active = False

        self.bullets = pygame.sprite.Group()

    def player_input(self):
        # pergerakan player sesuai input keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.move_ip(0, -5)
        if keys[pygame.K_s]:
            self.rect.move_ip(0, 5)
        if keys[pygame.K_a]:
            self.rect.move_ip(-5, 0)
        if keys[pygame.K_d]:
            self.rect.move_ip(5, 0)

            
    # batasan pergerakan player di layar game
    def player_constraint(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    # animasi player saat terbang dan menembak
    def animation_state(self):
        self.player_frame_index += 0.1
        if self.player_frame_index >= len(self.player_frames):
            self.player_frame_index = 0
        self.image = self.player_frames[int(self.player_frame_index)]
            

    def update(self):
        self.player_input()
        self.player_constraint()
        self.animation_state()

    def update_character(self):
        self.player_frames = []
        if self.character == 0:
            for i in range(1, 11):
                self.player_frames.append(pygame.image.load('graphics/player/naga_1/{}.png'.format(i)).convert_alpha())
        elif self.character == 1:
            for i in range(1, 11):
                self.player_frames.append(pygame.image.load('graphics/player/naga_2/{}.png'.format(i)).convert_alpha())
        else:
            for i in range(1, 11):
                self.player_frames.append(pygame.image.load('graphics/player/naga_3/{}.png'.format(i)).convert_alpha())
        self.player_frames = [pygame.transform.smoothscale(image, (110, 75)) for image in self.player_frames]
        self.player_frame_index = 0
        self.image = self.player_frames[self.player_frame_index]
        self.rect = self.image.get_rect(midbottom=(200, (SCREEN_HEIGHT / 2)))
        
    def change_character(self, new_character):
        self.character = new_character
        self.update_character()