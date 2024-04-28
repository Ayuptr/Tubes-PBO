import pygame
import os
from sys import exit
from random import randint
from player import Player
from meteor import Meteor
from star import Star
from cloud import Cloud
from button import Button

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
FPS = 60





class Game:
    def __init__(self):
        # game object setup
        self.character = 0
        player_sprite = Player(self.character)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.meteor = pygame.sprite.Group()
        self.star = pygame.sprite.Group()
        self.cloud = pygame.sprite.Group()

        # game condition and score
        self.game_active = False
        self.score = 0
        self.high_score = 0
        self.player_color = (255, 255, 255)
        self.background = 0

    # untuk mendapatkan font
    def get_font(self, size):
        return pygame.font.Font("font/kenvector_future_thin.ttf", size)
        
    # menampilkan score di dalam game
    def display_score(self):
        if self.background == 0:
            score_surf = self.get_font(25).render(f'Score: {self.score}', False, ('Black'))
        else:
            score_surf = self.get_font(25).render(f'Score: {self.score}', False, ('White'))
        score_rect = score_surf.get_rect(center = ((SCREEN_WIDTH/2), 30))
        screen.blit(score_surf, score_rect)

    # mengecek high score dari file highscore.txt
    def high_score_check(self):
        if os.path.exists('high_score.txt'):
            with open('high_score.txt', 'r') as file:
                # menginisiasi nilai high score dari file high_score.txt
                self.high_score = int(file.read())

    # mengecek apakah terjadi collision antara player dan meteor
    def collision_player(self):
        # jika terjadi collision maka akan mengosongkan semua grup objek
        if pygame.sprite.spritecollide(self.player.sprite, self.meteor, False):
            dead_sound.play()
            self.meteor.empty()
            self.star.empty()
            self.cloud.empty()
            self.player.sprite.bullets.empty()
            self.player.sprite.bullet_active = False
            self.player.sprite.indicator_active = False
            return False
        return True

    # mengecek apakah terjadi collision antara bullet dan meteor
    def collision_bullet(self):
        # jika terjadi collision maka akan akan menghapus objek bullet dari group
        for bullet in self.player.sprite.bullets:
            if pygame.sprite.spritecollide(bullet, self.meteor, True):
                explosion_sound.play()
                bullet.kill()
                return True
        return False


    def cheat(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            self.score += 1
        if keys[pygame.K_o]:
            self.game_active = False
            dead_sound.play()
            self.meteor.empty()
            self.star.empty()
            self.cloud.empty()
            self.player.sprite.bullets.empty()
            self.player.sprite.bullet_active = False

    # main game
    def main_game(self):
        bg_music.play(-1)
        wind_sound.play(-1)
        # game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if self.game_active:
                    # memunculkan objek sesuai timernya
                    if event.type == obstacle_timer:
                        self.meteor.add(Meteor(self.background))
                    if event.type == star_timer:
                        self.star.add(Star())
                    if event.type == cloud_timer:
                        self.cloud.add(Cloud(self.background))

            if self.game_active:
                if self.score > 50:
                    screen.blit(new_bg_surface, (0, 0))
                    self.background = 1
                else:
                    screen.blit(bg_surface, (0, 0))
                self.high_score_check()
                star_hit = pygame.sprite.spritecollide(self.player.sprite, self.star, True)
                # jika terjadi star_hit maka akan menambahkan score
                if star_hit:
                    star_sound.play()
                    self.score+=1

                # menjalankan semua method dari objek
                self.player.draw(screen)
                self.player.update()
                self.player.sprite.bullets.draw(screen)
                self.meteor.draw(screen)
                self.meteor.update()
                self.star.draw(screen)
                self.star.update()
                self.cloud.draw(screen)
                self.cloud.update()
                # menampilkan indicator dan score
                self.display_score()
                # jika bullet berhasil mengenai meteor maka akan menambahkan score
                if self.collision_bullet():
                    self.score += 10
                self.game_active = self.collision_player()
                self.cheat()

            # jika game tidak aktif maka akan menampilkan game over
            else:
                # mengupdate high score
                if self.score > self.high_score:
                    self.high_score = self.score
                    with open('high_score.txt', 'w') as file:
                        file.write(str(self.high_score))

                bg_music.stop()
                wind_sound.stop()
                self.game_over()

            pygame.display.update()
            clock.tick(FPS)

    # menampilkan game over screen
    def game_over(self):
        game_over_music.play()
        # tampilan untuk game over
        game_over_message = self.get_font(40).render('Game Over', True, (203,19,13))
        game_over_message_rect = game_over_message.get_rect(center = ((SCREEN_WIDTH/2), 100))
        score_massage = self.get_font(25).render(f'Your score: {self.score}', True, ('Black'))
        score_massage_rect = score_massage.get_rect(center = ((SCREEN_WIDTH/2), 200))
        high_score_message = self.get_font(18).render(f'High score: {self.high_score}', True, ('Black'))
        high_score_message_rect = high_score_message.get_rect(center = (700, 20))
        menu_message = self.get_font(15).render(f'esc to return to main menu', True, ('Black'))
        menu_message_rect = menu_message.get_rect(center = (140, 20))
        game_message = self.get_font(25).render('Press space to play again', True, ('Black'))
        game_message_rect = game_message.get_rect(center = ((SCREEN_WIDTH/2), 500))
        player_dead = pygame.image.load('graphics/player/dead.png').convert_alpha()
        player_dead = pygame.transform.rotozoom(player_dead, 0, 0.45)
        player_dead_rect = player_dead.get_rect(center = ((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2)))

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        run = False
                        self.game_active = True
                        game_over_music.stop()
                        self.score = 0
                        self.main_game()
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        game_over_music.stop()
                        self.main_menu()
                        
            # untuk menampilkan ke layar
            screen.blit(game_over_bg, (0, 0))
            screen.blit(game_over_message, game_over_message_rect)
            screen.blit(score_massage, score_massage_rect)
            screen.blit(high_score_message, high_score_message_rect)
            screen.blit(menu_message, menu_message_rect)
            screen.blit(game_message, game_message_rect)
            screen.blit(player_dead, player_dead_rect)

            pygame.display.update()

    # menampilkan main menu
    def main_menu(self):
        intro_music.play(-1)
        # tampilan untuk main menu
        title_text = self.get_font(45).render('Aircraft: Fly Forever', True, ('#cb130d'))
        title_rect = title_text.get_rect(center = (SCREEN_WIDTH/2, 200))
        menu_text = self.get_font(45).render("MAIN MENU", True, "Black")
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH/2, 300))
        copyright = self.get_font(35).render('Copyright © 2022 by Ganbaru Power', True, 'Black')
        copyright_rect = copyright.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-100))
        player_stand = pygame.image.load('graphics/player/naga_1/1.png').convert_alpha()
        player_stand =  pygame.transform.rotozoom(player_stand, 0, 0.45)
        player_stand_rect = player_stand.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-550))
        
        
        run = True
        while run:
            menu_mouse_pos = pygame.mouse.get_pos()
            # menginisiasi button untuk main menu
            play_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT-250), 
                                text_input="PLAY", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
            quit_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT-350), 
                                text_input="QUIT", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
            # Tombol untuk mengganti karakter
            prev_character_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH/2-250, SCREEN_HEIGHT-550),
                                text_input=">", font=self.get_font(20), base_color="Black", hovering_color="#baf4fc")
            next_character_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH/2+250, SCREEN_HEIGHT-550),
                                text_input=">", font=self.get_font(20), base_color="Black", hovering_color="#baf4fc")

            # menampilkan ke layar
            screen.blit(intro_bg, (0, 0))
            screen.blit(title_text, title_rect)
            screen.blit(player_stand, player_stand_rect)
            screen.blit(menu_text, menu_rect)
            screen.blit(copyright, copyright_rect)

            # update button
            for button in [play_button, quit_button,next_character_button,prev_character_button]:
                button.change_color(menu_mouse_pos)
                button.update(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # untuk mengecek apakah tombol diklik
                    if play_button.check_for_input(menu_mouse_pos):
                        run = False
                        intro_music.stop()
                        self.game_active = True
                        self.main_game()
                    if next_character_button.check_for_input(menu_mouse_pos):
                        self.character = (self.character + 1) % 3
                        self.player.sprite.change_character(self.character)
                        if self.character == 0:
                            player_stand = pygame.image.load('graphics/player/naga_1/1.png').convert_alpha()
                        elif self.character == 1:
                            player_stand = pygame.image.load('graphics/player/naga_2/1.png').convert_alpha()
                        else:
                            player_stand = pygame.image.load('graphics/player/naga_3/1.png').convert_alpha()
                        player_stand = pygame.transform.rotozoom(player_stand, 0, 0.45)
                        player_stand_rect = player_stand.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-550))
                    if prev_character_button.check_for_input(menu_mouse_pos):
                        self.character = (self.character - 1) % 3
                        self.player.sprite.change_character(self.character)
                        if self.character == 0:
                            player_stand = pygame.image.load('graphics/player/naga_1/1.png').convert_alpha()
                        elif self.character == 1:
                            player_stand = pygame.image.load('graphics/player/naga_2/1.png').convert_alpha()
                        else:
                            player_stand = pygame.image.load('graphics/player/naga_3/1.png').convert_alpha()
                        player_stand = pygame.transform.rotozoom(player_stand, 0, 0.45)
                        player_stand_rect = player_stand.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-550))
                    if quit_button.check_for_input(menu_mouse_pos):
                        pygame.quit()
                        exit()

            pygame.display.update()
    
    # menjalankan game
    def run(self):
        self.main_menu()

# inisiasi game
pygame.init()
pygame.display.set_caption('Aircraft: Fly Forever')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# timer kemunculan objek
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, randint(1000, 1500))
star_timer = pygame.USEREVENT + 2
pygame.time.set_timer(star_timer, randint(1000, 1500))
cloud_timer = pygame.USEREVENT + 3
pygame.time.set_timer(cloud_timer, randint(2000, 2500))

# game additonal setup
bg_surface = pygame.image.load('graphics/background.png').convert_alpha()
bg_surface = pygame.transform.smoothscale(bg_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
new_bg_surface = pygame.image.load('graphics/background_2.png').convert_alpha()
new_bg_surface = pygame.transform.smoothscale(new_bg_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
intro_bg = pygame.image.load('graphics/intro_bg.png').convert_alpha()
intro_bg = pygame.transform.smoothscale(intro_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_over_bg = pygame.image.load('graphics/game_over_bg.png').convert_alpha()
game_over_bg = pygame.transform.smoothscale(game_over_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
indicator = pygame.image.load('graphics/player/intro.png').convert_alpha()
indicator = pygame.transform.smoothscale(indicator, (55, 37))
indicator_rect = indicator.get_rect(center = (40, 30))

# audio setup
bg_music = pygame.mixer.Sound('audio/airship.flac')
bg_music.set_volume(0.5)
intro_music = pygame.mixer.Sound('audio/happy.mp3')
intro_music.set_volume(0.5)
game_over_music = pygame.mixer.Sound('audio/sunshine.mp3')
game_over_music.set_volume(0.5)
star_sound = pygame.mixer.Sound('audio/star.mp3')
star_sound.set_volume(0.5)
explosion_sound = pygame.mixer.Sound('audio/explosion.flac')
explosion_sound.set_volume(0.5)
dead_sound = pygame.mixer.Sound('audio/dead.flac')
dead_sound.set_volume(0.5)
wind_sound = pygame.mixer.Sound('audio/wind.wav')
wind_sound.set_volume(0.5)

# game run
game = Game()
game.run()