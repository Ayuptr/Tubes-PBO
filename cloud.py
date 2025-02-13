import pygame
from random import randint

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

class Cloud(pygame.sprite.Sprite):
    def __init__(self,background):
        super().__init__()
        self.cloud_frames = []
        self.rand_int = randint(1,2)
        if(background == 0):
            for i in range(1, 4):
                self.cloud_frames.append(pygame.image.load('graphics/clouds/cloud{}.png'.format(i)).convert_alpha())
        else:
            for i in range(1, 4):
                self.cloud_frames.append(pygame.image.load('graphics/clouds/cloud_dark_{}.png'.format(i)).convert_alpha())
        self.cloud_frames = [pygame.transform.smoothscale(image, (95, 63)) for image in self.cloud_frames]
        self.cloud_frame_index = 0

        self.image = self.cloud_frames[self.cloud_frame_index]
        self.rect = self.image.get_rect(bottomright = (randint(1350, 1500), randint(60, SCREEN_HEIGHT)))

    # animasi cloud
    def animation_state(self):
        self.cloud_frame_index += 0.1
        if self.cloud_frame_index >= len(self.cloud_frames):
            self.cloud_frame_index = 0
        self.image = self.cloud_frames[int(self.cloud_frame_index)]

    # menghapus cloud jika sudah keluar layar
    def destroy(self):
        if self.rect.left <= -100:
            self.kill()
    
    def update(self):
        self.animation_state()
        self.rect.move_ip(-5, 0)
        self.destroy()