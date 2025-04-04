import pygame, sys
from pygame.locals import *
import random, time
pygame.init()
FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0
COINS_TO_INCREASE_SPEED = 5 #add speed after 5coins
WHITE=(255, 255, 255)
BLACK=(0, 0, 0)
RED =(255, 0, 0)
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
#screen 
background = pygame.image.load("AnimatedStreet.png")
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Game")
FramePerSec = pygame.time.Clock()
#enemy car
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
#player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)
#Coin with dif weights
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = random.choice([1, 2, 3])
        self.image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.reset_position()
    def reset_position(self):
        self.weight = random.choice([1, 2, 3])  #random weight(from 1to3)
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
    def move(self):
        self.rect.move_ip(0, SPEED // 2)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()
#init. bjects
P1=Player()
E1=Enemy()
C1=Coin()
#sprite groups
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
enemies.add(E1)
coins.add(C1)
all_sprites.add(P1, E1, C1)
#game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    DISPLAYSURF.blit(background, (0, 0))#background
    #display score/coins
    score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 120, 10))
    #move and draw sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)
    #collision with car
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(1)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()
    #collision with coin
    if pygame.sprite.spritecollideany(P1, coins):
        COINS_COLLECTED += C1.weight
        C1.reset_position()
        if COINS_COLLECTED % COINS_TO_INCREASE_SPEED == 0:
            SPEED += 1  #increase speed
    pygame.display.update()
    FramePerSec.tick(FPS)
pygame.quit()