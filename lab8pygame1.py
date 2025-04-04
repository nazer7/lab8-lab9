# Imports
import pygame, sys
from pygame.locals import *
import random, time
# Initializing 
pygame.init()
# Setting up FPS 
FPS= 60
FramePerSec= pygame.time.Clock()
# Colors
BLUE=(0, 0, 255)
RED=(255, 0, 0)
GREEN=(0, 255, 0)
BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
# Screen settings
SCREEN_WIDTH=400
SCREEN_HEIGHT=600
SPEED=5
SCORE=0
COINS_COLLECTED = 0  # Количество собранных монет
# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
# Load background image
background = pygame.image.load("AnimatedStreet.png")
# Create a display surface
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
# Enemy class (other cars)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        #Move enemy downwards and reset position if off screen.
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
# Player class (our car)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)   
    def move(self):
        #Handle player movement based on key presses.
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
# Coin class (randomly appearing coins)
# Coin class (moving coins)
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.image.set_colorkey((255, 255, 255)) 
        # Уменьшаем размер 
        self.image = pygame.transform.scale(self.image, (30, 30))  
        self.rect = self.image.get_rect()
        self.reset_position()
    def reset_position(self):
        """Move coin to a random position at the top of the screen."""
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
    def move(self):
        """Move coin down like an enemy car."""
        self.rect.move_ip(0, SPEED // 2)  # Монеты падают медленнее врагов
        if self.rect.top > SCREEN_HEIGHT:  # Если монета уходит за экран — ресет
            self.reset_position()
# Initialize player, enemy, and coin
P1 = Player()
E1 = Enemy()
C1 = Coin()
# Create sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
# Custom event for increasing speed
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
# Game Loop
while True:    
    # Handle events
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5      
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # Draw background
    DISPLAYSURF.blit(background, (0, 0))
    # Draw scores
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    coins_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 100, 10))
    # Move and redraw all sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)
    # Check for collision between player and enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(1)          
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250)) 
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()        
    # Check for collision between player and coin
    if pygame.sprite.spritecollideany(P1, coins):
        COINS_COLLECTED += 1
        C1.reset_position()  # Move coin to a new position
    # Update the display
    pygame.display.update()
    FramePerSec.tick(FPS)



