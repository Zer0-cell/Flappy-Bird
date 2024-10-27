import pygame, random, time
from pygame.locals import *

SCREEN_WIDHT = 400
SCREEN_HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15

GROUND_WIDHT = 2 * SCREEN_WIDHT
GROUND_HEIGHT = 100

PIPE_WIDHT = 80
PIPE_HEIGHT = 500

PIPE_GAP = 150

wing = 'assets/audio/wing.wav'
hit = 'assets/audio/hit.wav'

pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird by Zer0')

BACKGROUND = pygame.image.load('assets/images/background.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDHT, SCREEN_HEIGHT))

BEGIN_IMAGE = pygame.image.load('assets/images/message.png').convert_alpha()

GAME_OVER_IMAGE = pygame.image.load('assets/images/gameover.png').convert_alpha()
GAME_OVER_IMAGE = pygame.transform.scale(GAME_OVER_IMAGE, (200, 100))

score_images = [pygame.image.load(f'assets/images/{i}.png').convert_alpha() for i in range(10)]

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load('assets/images/bluebird-upflap.png').convert_alpha(),
                       pygame.image.load('assets/images/bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('assets/images/bluebird-downflap.png').convert_alpha()]
        
        self.speed = SPEED
        self.current_image = 0
        self.image = self.images[self.current_image]
        
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        
        self.rect[0] = SCREEN_WIDHT / 6
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        
        self.speed += GRAVITY
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

    def begin(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/images/pipe.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDHT, PIPE_HEIGHT))
        
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/images/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDHT, GROUND_HEIGHT))
        
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    
    return pipe, pipe_inverted

def draw_score(screen, score, y_pos=20):
    x_pos = 20
    for digit in str(score):
        screen.blit(score_images[int(digit)], (x_pos, y_pos))
        x_pos += score_images[int(digit)].get_width()

def show_game_over_screen(final_score):
    screen.blit(GAME_OVER_IMAGE, (100, 200))
    
    total_width = sum(score_images[int(digit)].get_width() for digit in str(final_score))
    x_pos = (SCREEN_WIDHT - total_width) // 2  # Center the score

    for digit in str(final_score):
        screen.blit(score_images[int(digit)], (x_pos, 300))
        x_pos += score_images[int(digit)].get_width()

    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    exit()


bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDHT * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDHT * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()
begin = True
score = 0

while begin:
    clock.tick(15)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird.bump()
                
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()
                begin = False
    
    screen.blit(BACKGROUND, (0, 0))
    screen.blit(BEGIN_IMAGE, (120, 150))
    
    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(GROUND_WIDHT - 20)
        ground_group.add(new_ground)
    
    bird.begin()
    ground_group.update()
    
    bird_group.draw(screen)
    ground_group.draw(screen)
    pygame.display.update()

while True:
    clock.tick(15)
    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
        
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird.bump()
                
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()

    screen.blit(BACKGROUND, (0, 0))
    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(GROUND_WIDHT - 20)
        ground_group.add(new_ground)
    
    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])
        
        pipes = get_random_pipes(SCREEN_WIDHT * 2)
        
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    for pipe in pipe_group:
        if pipe.rect.right < bird.rect.left and not hasattr(pipe, 'scored'):
            score += 1
            pipe.scored = True

    bird_group.update()
    ground_group.update()
    
    pipe_group.update()
    bird_group.draw(screen)
    
    pipe_group.draw(screen)
    ground_group.draw(screen)
    
    draw_score(screen, score)
    pygame.display.update()

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        pygame.mixer.music.load(hit)
        pygame.mixer.music.play()
        show_game_over_screen(score)
