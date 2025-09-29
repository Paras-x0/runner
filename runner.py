import pygame
import sys
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0
        self.jump_count = 0
        self.jump_sound = pygame.mixer.Sound('music/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self, events):
        global initial_score
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.jump_count < 2:
                    self.gravity = -20
                    self.jump_count += 1
                    initial_score += 100
                    self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.gravity = 0
            self.jump_count = 0
        elif self.rect.top <= 0:
            self.rect.top = 0
            self.gravity = 1

    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.apply_gravity()
        self.animation()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_frame1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 210
        else:
            snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    score_surface = test_font.render(str(initial_score), False, 'Black')
    score_rect = score_surface.get_rect(center=(500, 50))
    pygame.draw.rect(screen, '#c0e8ec', score_rect)
    pygame.draw.rect(screen, '#c0e8ec', score_rect, 8)
    screen.blit(score_surface, score_rect)


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


# Game Setup
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
pygame.display.set_caption("Runner")

game_active = False
initial_score = 0
bg_music = pygame.mixer.Sound('music/music.wav')
bg_music.set_volume(0.5)
bg_music.play()

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Background
sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

# Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_transform = pygame.transform.scale(player_stand, (100, 100))
player_stand_rect = player_stand_transform.get_rect(center=(400, 200))

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
test_font1 = pygame.font.Font('font/Pixeltype.ttf', 40)
intro_surface = test_font1.render('press  SPACE  to  start', False, 'Black')
intro_rect = intro_surface.get_rect(midbottom=(430, 300))

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# Main loop
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active:
                    game_active = True
                    initial_score = 0
                    obstacle_group.empty()
                    player.sprite.rect.midbottom = (80, 300)
                    player.sprite.gravity = 0
                    player.sprite.jump_count = 0

        if event.type == obstacle_timer and game_active:
            obstacle_group.add(Obstacle(choice(['snail', 'fly', 'snail', 'snail'])))

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        display_score()

        player.sprite.player_input(events)  
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()
    else:
        screen.fill('#c0e8ec')
        screen.blit(player_stand_transform, player_stand_rect)
        screen.blit(intro_surface, intro_rect)

    pygame.display.update()
    clock.tick(60)
