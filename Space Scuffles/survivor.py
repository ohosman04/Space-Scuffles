
import pygame
import os
import random
from pygame import mixer
pygame.font.init()
pygame.mixer.init()
mixer.init()
mixer.music.load(os.path.join('Assets','Music2.mp3'))
mixer.music.play(-1)

HEALTH_FONT = pygame.font.Font(os.path.join('Fonts','yoster.ttf'), 40)
SCORE_FONT = pygame.font.Font(os.path.join('Fonts','yoster.ttf'), 40)
END_FONT = pygame.font.Font(os.path.join('Fonts','yoster.ttf'), 100)

WIDTH,HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Survivor")

RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,150,255)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Collision.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','Shoot.mp3'))
COIN_SOUND = pygame.mixer.Sound(os.path.join('Assets','Coin.mp3'))


FPS = 60
SPACESHIP_WIDTH,SPACESHIP_HEIGHT = 55,40

YELLOW_HIT = pygame.USEREVENT + 1
COLLECT_EGG = pygame.USEREVENT + 2

VEL = 5
BULLETS_VEL = 7
MAX_BULLETS = 30

EGG_WIDTH,EGG_HEIGHT = 20,25

random_x = random.randint(50,850)
random_y = random.randint(50,450)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space2.jpg')),(WIDTH,HEIGHT))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 0)

EGG_IMAGE = pygame.image.load(os.path.join('Assets','egg.png'))
EGG = pygame.transform.scale(EGG_IMAGE,(EGG_WIDTH,EGG_HEIGHT))

def draw_window(egg,yellow,bullets,yellow_health,score):
    WIN.blit(SPACE,(0,0))

    health_text = HEALTH_FONT.render(f'Health: {str(yellow_health)}',1,WHITE)
    score_text = SCORE_FONT.render(f'Score: {str(score)}',1,WHITE)
    WIN.blit(score_text,(WIDTH-score_text.get_width() - 10, 10))
    WIN.blit(health_text, (10,10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x,yellow.y))
    WIN.blit(EGG,(egg.x,egg.y))

    for bullet in bullets:
        pygame.draw.rect(WIN,RED,bullet)
    pygame.display.update()

def handle_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL < HEIGHT - SPACESHIP_HEIGHT - 10:
        yellow.y += VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL < WIDTH - SPACESHIP_WIDTH:
        yellow.x += VEL

def handle_bullets(bullets,yellow):
    for bullet in bullets:
        bullet.y -= BULLETS_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            bullets.remove(bullet)
        if bullet.y < 0:
            bullets.remove(bullet)
def handle_eggs(eggs,yellow):
    for egg in eggs:
        random_cordx = random.randint(50,850)
        random_cordy = random.randint(50,450)
        if yellow.colliderect(egg):
            pygame.event.post(pygame.event.Event(COLLECT_EGG))
            egg.x = random_cordx
            egg.y = random_cordy
            eggs.remove(egg)
            eggs.append(egg)

def draw_winner(text):
    draw_text = END_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH / 2 - draw_text.get_width() / 2, HEIGHT /2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    yellow = pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    egg = pygame.Rect(random_x,random_y,EGG_WIDTH,EGG_HEIGHT)
    eggs = [egg]
    clock = pygame.time.Clock()
    run = True

    yellow_health = 10
    score = 0
    bullets = []
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(random.randint(10,890),490,5,10)
                    bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == COLLECT_EGG:
                score += 1
                COIN_SOUND.play()
            
        if yellow_health <= 0:
            end_text = 'Game over...'
            draw_winner(end_text)
            break
        
        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed,yellow)
        handle_eggs(eggs,yellow)
        handle_bullets(bullets,yellow)
        draw_window(egg,yellow,bullets,yellow_health,score)
        
    main()

if __name__ == "__main__":
    main()