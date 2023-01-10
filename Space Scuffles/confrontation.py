
import pygame
import os
from pygame import mixer
pygame.font.init() #initialize pygame font library
pygame.mixer.init() #initialize sound
mixer.init()
mixer.music.load(os.path.join('Assets','Music.mp3'))
mixer.music.play(-1)

WIDTH, HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Battle")

BLUE = (100,150,200)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,10)
WHITE = (255,255,255)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55,40
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5


YELLOW_HIT = pygame.USEREVENT + 1 #represents code or number of user events
RED_HIT = pygame.USEREVENT + 2    #add 2 to this one because different events

BORDER = pygame.Rect((WIDTH//2 - 5), 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Collision.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','Shoot.mp3'))

HEALTH_FONT = pygame.font.Font(os.path.join('Fonts','yoster.ttf'), 40)
WINNER_FONT = pygame.font.Font(os.path.join('Fonts','yoster.ttf'), 100)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)


RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.jpg')),(WIDTH,HEIGHT))


def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)

    red_health_text = HEALTH_FONT.render(f"Health: {str(red_health)}",1, WHITE) #args: string,anti-aliasing(always 1), color
    yellow_health_text = HEALTH_FONT.render(f"Health: {str(yellow_health)}",1, WHITE) 
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10,10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x,yellow.y)) #use when you want to load in a surface
    WIN.blit(RED_SPACESHIP, (red.x,red.y)) #args: what we wanna draw, where on x and y as tuple


    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet) #args: where is it drawn, what color, what are we drawing
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #Left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x : #Right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #Up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height <HEIGHT - 15: #Down
        yellow.y += VEL
def red_handle_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #Left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH : #Right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #Up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height <HEIGHT - 15: #Down
        red.y += VEL

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL #left to right
        if red.colliderect(bullet): #if rect of red collided with bullet
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
                yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL #right to left
        if yellow.colliderect(bullet): #if rect of red collided with bullet
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
                red_bullets.remove(bullet)
def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH / 2 - draw_text.get_width()/ 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000) #pauses game to show winner for 5 seconds

def main():
    red = pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)#args: x,y,width,height
    yellow = pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) #never goes over 60fps
        for event in pygame.event.get(): #gets a list of events were looping thru and check what the events are.
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN and len(yellow_bullets) < MAX_BULLETS:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height// 2 - 2,10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height// 2 - 2,10,5) #no plus width because its from the left aslan
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
            
        winner_text = ''    
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        
        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != '':
            draw_winner(winner_text)
            break


        keys_pressed = pygame.key.get_pressed() #tells us thruout loop what keys are getting pressed
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)

        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        
        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)

    main()

if __name__ == '__main__':
    main()
