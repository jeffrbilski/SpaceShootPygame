import pygame
import os # Allows us to define paths to assets
pygame.font.init()
pygame.mixer.init()

"""
@Notes:
pygame is a 2d graphics library
"""

'''
@constants
'''
WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)
HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT = pygame.font.SysFont('comicsans', 60)
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "explosion-91872.mp3"))
BULLET_SHOOT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "laser-shot-ingame-230500.mp3"))

FPS_60 = 60
MAX_BULLETS = 3
BULLET_VEL = 7
VEL = 5
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40

# Events
# USEREVENT is a number, we add to it to make it a unique number
Y_HIT = pygame.USEREVENT + 1
R_HIT = pygame.USEREVENT + 2

# Obtain image assets
YELLOW_SPACESHIP_IMG = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
RED_SPACESHIP_IMG = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))

# Resize images
YELLOW_SPACESHIP_IMG = pygame.transform.scale(YELLOW_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP_IMG = pygame.transform.scale(RED_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

# Rotate images
YELLOW_SPACESHIP_IMG = pygame.transform.rotate(YELLOW_SPACESHIP_IMG, 90)
RED_SPACESHIP_IMG = pygame.transform.rotate(RED_SPACESHIP_IMG, 270)

# Set the title on the window frame
pygame.display.set_caption("First Game!")

BG_IMAGE = pygame.image.load(os.path.join('Assets', 'space.png'))
BG = pygame.transform.scale(BG_IMAGE, (WIDTH, HEIGHT))

'''
@brief
    draws the window based on the conditions of the red and yellow player.
    Is called every cycle of the game loop
'''
def draw_window(red, yellow, r_bullets, y_bullets, r_health, y_health):
    WINDOW.blit(BG, (0,0))                                  # Draw the background "surface"
    pygame.draw.rect(WINDOW, BLACK, BORDER)                 # Draw the dividing border
    WINDOW.blit(RED_SPACESHIP_IMG, (red.x, red.y))          # Draws the red player "surface"
    WINDOW.blit(YELLOW_SPACESHIP_IMG, (yellow.x, yellow.y)) # Draws the yellow player "surface"

    r_health_text = HEALTH_FONT.render("Health: " + str(r_health), 1, WHITE) # The 1 is for anti-aliasing
    y_health_text = HEALTH_FONT.render("Health: " + str(y_health), 1, WHITE) # The 1 is for anti-aliasing
    WINDOW.blit(r_health_text, (WIDTH - r_health_text.get_width() - 10, 10))
    WINDOW.blit(y_health_text, (10, 10))

    for bullet in r_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    for bullet in y_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    pygame.display.update()

'''
@brief
    handles a yellow player's movement
'''
def handle_yellow_move(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: # down
        yellow.y += VEL

'''
@brief
    handles a red player's movement
'''
def handle_red_move(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL - red.width > BORDER.x: # left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL < WIDTH: # right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: # down
        red.y += VEL
'''
@brief
    this processes bullet movement and checks if it hits a player
'''
def handle_bullets(y_bullets, r_bullets, yellow, red):
    for bullet in y_bullets:
        bullet.x += BULLET_VEL

        #pygame method that checks for collision between rectangles
        if red.colliderect(bullet):
            #create an event
            pygame.event.post(pygame.event.Event(R_HIT))
            y_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            y_bullets.remove(bullet)

    for bullet in r_bullets:
        bullet.x -= BULLET_VEL

        #pygame method that checks for collision between rectangles
        if yellow.colliderect(bullet):
            #create an event
            pygame.event.post(pygame.event.Event(Y_HIT))
            r_bullets.remove(bullet)
        elif bullet.x < 0:
            r_bullets.remove(bullet)

'''
@brief
    this draws the "winner" text in the event that a player wins.
'''
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE) # 1 for anti-aliasing
    width = WIDTH//2 - draw_text.get_width()//2 # Calculate center width
    height = HEIGHT//2
    WINDOW.blit(draw_text, (width, height))

    # Update the display and pause the game 5 seconds
    pygame.display.update()
    pygame.time.delay(5000)

'''
@brief
    The game's main function
'''
def main():
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    r_bullets = []
    y_bullets = []

    r_health = 10
    y_health = 10

    clock = pygame.time.Clock()
    run = True

    while run:
        #This ensures we don't draw the screen more than 60 FPS
        clock.tick(FPS_60)

        # Very important for Pygame: provides list of all event changes in the game
        for event in pygame.event.get():
            # this is when the user clicks the 'x' on the window
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(y_bullets) < MAX_BULLETS:
                    # create a bullet at yellow's location
                    # width = 10pixels, height = 5pixels
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    y_bullets.append(bullet)
                    BULLET_SHOOT_SOUND.play()

                if event.key == pygame.K_RCTRL and len(r_bullets) < MAX_BULLETS:
                    # create a bullet at yellow's location
                    # width = 10pixels, height = 5pixels
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    r_bullets.append(bullet)
                    BULLET_SHOOT_SOUND.play()

            if event.type == R_HIT:
                r_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == Y_HIT:
                y_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if r_health <= 0:
            winner_text = "Yellow Wins!"
        if y_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        #tells us what keys were pressed down
        keys_pressed = pygame.key.get_pressed()

        # Process player moves
        handle_yellow_move(keys_pressed, yellow)
        handle_red_move(keys_pressed, red)

        handle_bullets(y_bullets, r_bullets, yellow, red)

        draw_window(red, yellow, r_bullets, y_bullets, r_health, y_health)


    pygame.quit()

# Python will automatically run "main()" if the file is imported.
# Doing this will prevent that, so main will only run if this file is run directly.
if __name__ == "__main__":
    main()
