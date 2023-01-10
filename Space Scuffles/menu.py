def confrontation():
    import pygame
    import os
    from pygame import mixer
    from button import Button
    pygame.font.init() #initialize pygame font library
    pygame.mixer.init() #initialize sound
    mixer.init()
    mixer.music.load(os.path.join('Assets','Music.mp3'))
    mixer.music.play(-1)

    
    GAMES_FONT = pygame.font.Font(os.path.join('Fonts','INVASION2000.ttf'),40)

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
    WINNER_FONT = pygame.font.Font(os.path.join('Fonts','INVASION2000.ttf'), 100)

    YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
    YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)


    RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
    RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 270)

    SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.jpg')),(WIDTH,HEIGHT))

    def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health,button):
        WIN.blit(SPACE, (0,0))
        pygame.draw.rect(WIN,BLACK,BORDER)

        red_health_text = HEALTH_FONT.render(f"Health: {str(red_health)}",1, WHITE) #args: string,anti-aliasing(always 1), color
        yellow_health_text = HEALTH_FONT.render(f"Health: {str(yellow_health)}",1, WHITE) 
        button.update(WIN)
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
        draw_text = WINNER_FONT.render(text,1,'Cyan')
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
        button = Button(image=None,pos=(WIDTH/2,25),text_input="BACK",font=GAMES_FONT,base_color='Gray',hovering_color=BLUE)
        while run:
            
            clock.tick(FPS) #never goes over 60fps
            PLAY_MOUSE_POS = pygame.mouse.get_pos()

            button.changeColor(PLAY_MOUSE_POS)
            

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button.checkForInput(PLAY_MOUSE_POS):
                        main_menu()
            

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

            draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health,button)

        main()
    if __name__ == '__main__':
        main()

def survivor():
    import pygame
    import os
    import random
    from pygame import mixer
    from button import Button
    pygame.font.init()
    pygame.mixer.init()
    mixer.init()
    mixer.music.load(os.path.join('Assets','Music2.mp3'))
    mixer.music.play(-1)

    HEALTH_FONT = pygame.font.Font(os.path.join('Fonts','yoster.ttf'), 40)
    SCORE_FONT = pygame.font.Font(os.path.join('Fonts','yoster.ttf'), 40)
    END_FONT = pygame.font.Font(os.path.join('Fonts','INVASION2000.ttf'), 100)

    WIDTH,HEIGHT = 900,500
    WIN = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Space Survivor")

    RED = (255,0,0)
    YELLOW = (255,255,0)
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    BLUE = (100,150,255)

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

    GAMES_FONT = pygame.font.Font(os.path.join('Fonts','INVASION2000.ttf'),40)


    def draw_window(egg,yellow,bullets,yellow_health,score,button):
        WIN.blit(SPACE,(0,0))

        health_text = HEALTH_FONT.render(f'Health: {str(yellow_health)}',1,WHITE)
        score_text = SCORE_FONT.render(f'Score: {str(score)}',1,WHITE)
        WIN.blit(score_text,(WIDTH-score_text.get_width() - 10, 10))
        WIN.blit(health_text, (10,10))
        button.update(WIN)
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

        button = Button(image=None,pos=(WIDTH/2,25),text_input="BACK",font=GAMES_FONT,base_color=WHITE,hovering_color=BLUE)
        while run:
            clock.tick(FPS)
            PLAY_MOUSE_POS = pygame.mouse.get_pos()
            button.changeColor(PLAY_MOUSE_POS)
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button.checkForInput(PLAY_MOUSE_POS):
                        main_menu()
                    

            if yellow_health <= 0:
                end_text = 'Game over...'
                draw_winner(end_text)
                break
            
            keys_pressed = pygame.key.get_pressed()
            handle_movement(keys_pressed,yellow)
            handle_eggs(eggs,yellow)
            handle_bullets(bullets,yellow)
            draw_window(egg,yellow,bullets,yellow_health,score,button)

        main()

    if __name__ == "__main__":
        main()

def main_menu():
    from button import Button
    import pygame
    import os
    import sys
    from pygame import mixer
    pygame.mixer.init()
    pygame.font.init()
    mixer.music.load(os.path.join('Assets','Music3.mp3'))
    mixer.music.play(-1)
    
    WIDTH,HEIGHT = 900,500
    WIN = pygame.display.set_mode((WIDTH,HEIGHT))
    BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets','cyanbg.jpg')),(WIDTH,HEIGHT))

    MENU_FONT = pygame.font.Font(os.path.join('Fonts','INVASION2000.ttf'),50)
    GAMES_FONT = pygame.font.Font(os.path.join('Fonts','INVASION2000.ttf'),20)

    WHITE = (255,255,255)
    BLACK = (0,0,0)

    pygame.display.set_caption("Menu")
    run  = True
    while run:
        WIN.blit(BG, (0,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = MENU_FONT.render("SPACE SCUFFLES", True, BLACK)
        MENU_RECT = MENU_TEXT.get_rect(center = (WIDTH /2,50))

        CONFRONT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load(os.path.join('Assets','Play Rect.png')),(200,75)),pos=(WIDTH/2,200),text_input="Confrontation",font=GAMES_FONT,base_color=BLACK,hovering_color=WHITE)
        SURVIVOR_BUTTON = Button(image=pygame.transform.scale(pygame.image.load(os.path.join('Assets','Options Rect.png')),(200,75)),pos=(WIDTH/2,300),text_input="Survivor",font=GAMES_FONT,base_color=BLACK,hovering_color=WHITE)
        QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load(os.path.join('Assets','Quit Rect.png')),(200,75)),pos=(WIDTH/2,400),text_input="Quit",font=GAMES_FONT,base_color=BLACK,hovering_color=WHITE)

        WIN.blit(MENU_TEXT,MENU_RECT)

        for button in [CONFRONT_BUTTON,SURVIVOR_BUTTON,QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CONFRONT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mixer.music.set_volume(100)
                    confrontation()
                if SURVIVOR_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mixer.music.set_volume(100)
                    survivor()
                    
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
    

if __name__ == '__main__':
    main_menu()
