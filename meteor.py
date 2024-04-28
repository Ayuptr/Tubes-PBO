import pygame
from random import randint

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

class Meteor(pygame.sprite.Sprite):
    def __init__(self,background):
        super().__init__()
        self.misil_frames = []
        self.rand_int = randint(1,2)
        if(background == 0):
            for i in range(1, 4):
                self.misil_frames.append(pygame.image.load('graphics/misil/meteor_1.png').convert_alpha())
        else:
            for i in range(1, 4):
                self.misil_frames.append(pygame.image.load('graphics/misil/meteor_2.png').convert_alpha())
        self.misil_frames = [pygame.transform.smoothscale(image, (150, 90)) for image in self.misil_frames]
        self.misil_frame_index = 0
        
        self.image = self.misil_frames[self.misil_frame_index]
        self.rect = self.image.get_rect(bottomright = (randint(1350, 1500), randint(50, SCREEN_HEIGHT)))
        self.vel = randint(4, 7)

    # animasi misil
    def animation_state(self):
        self.misil_frame_index += 1
        if self.misil_frame_index >= len(self.misil_frames):
            self.misil_frame_index = 0
        self.image = self.misil_frames[self.misil_frame_index]

    # menghapus misil jika sudah keluar layar
    def destroy(self):
        if self.rect.left <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= self.vel
        self.destroy()