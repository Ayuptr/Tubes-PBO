import pygame
from random import randint

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.coin_frames = []
        for i in range(2,11):
            self.coin_frames.append(pygame.image.load('graphics/coin/{}.png'.format(i)).convert_alpha())
        self.coin_frames = [pygame.transform.smoothscale(image, (69, 63)) for image in self.coin_frames]
        self.coin_frame_index = 0

        self.image = self.coin_frames[self.coin_frame_index]
        self.rect = self.image.get_rect(bottomright = (randint(1350, 1500), randint(60, SCREEN_HEIGHT)))
        self.vel = randint(4, 7)
        self.last_frame_update = pygame.time.get_ticks()  # Waktu terakhir animasi diperbarui

        # Penundaan antara perubahan frame (ms)
        self.animation_delay = 100  # Misalnya, 100 ms


    # animasi coin
    def animation_state(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_update >= self.animation_delay:
            self.coin_frame_index += 1
            if self.coin_frame_index >= 9:
                self.coin_frame_index = 0
            self.image = self.coin_frames[self.coin_frame_index]
            self.last_frame_update = current_time

    # menghapus coin jika sudah keluar layar
    def destroy(self):
        if self.rect.left <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= self.vel
        self.destroy()