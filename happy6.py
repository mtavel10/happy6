import pygame
import sys, random, time

# CONSTANTS
WIDTH = 800
HEIGHT = 600
OB_SPEED = 5
ROUNDS = 25
GROUND = 425

#Before game loop things
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect()
clock = pygame.time.Clock()
running = True
round_count = 0
game_state = "start menu"
falling_objects = []
bg_img = pygame.transform.scale(pygame.image.load("minecraftbackground.jpg"), (WIDTH, HEIGHT))

class obstacle():
    def __init__(self):
        self.SURFACE = pygame.transform.scale(pygame.image.load("tnt.png"), (35, 35))
        self.rect = pygame.Rect(random.randint(0, WIDTH - 50), 0, 35, 35)
    def draw(self, screen, x=0, y=0):
        self.rect.x += x
        self.rect.y += y
        screen.blit(self.SURFACE, self.rect)
    
class envelope():
    def __init__(self):
        self.SURFACE = pygame.transform.scale(pygame.image.load("envelope.png"), (65, 40))
        self.rect = pygame.Rect(WIDTH/2, 0, 50, 50)
    def draw(self, screen, x=0, y=0):
        self.rect.x += x
        self.rect.y += y
        screen.blit(self.SURFACE, self.rect)
    def open(self, screen):
        font = pygame.font.SysFont('arial', 40)
        title = font.render("letter text", True, "black", "white")
        msg_rect = pygame.Rect(WIDTH/5, HEIGHT/5, 300, 300)
        screen.blit(title, msg_rect)

def draw_start_menu(message1: str, message2: str):
    screen.fill("white")
    screen.blit(bg_img, screen_rect)
    font = pygame.font.SysFont('arial', 40)
    title = font.render(message1, True, "black")
    start_button = font.render(message2, True, "black")
    screen.blit(title, (WIDTH/2 - title.get_width()/2, HEIGHT/2 - title.get_height()/2))
    screen.blit(start_button, (WIDTH/2 - start_button.get_width()/2, HEIGHT/2 + start_button.get_height()/2))
    pygame.display.update()

START_POSITION = (400, GROUND)
PAULINA_SURFACE = pygame.transform.scale(pygame.image.load("paulina.png"), (64, 88))
paulina_rect = PAULINA_SURFACE.get_rect(center=START_POSITION)

letter = envelope()

while running:
    for event in pygame.event.get(): 
       if event.type == pygame.QUIT:
           pygame.quit()
           quit()
    
    keys = pygame.key.get_pressed()
    
    if game_state == "start menu":
        draw_start_menu("happy six months <3", "press space to start")
        if keys[pygame.K_SPACE]:
            paulina_rect.x, paulina_rect.y = START_POSITION
            game_state = "game"
    
    #Game started
    if game_state == "game": 
    
        # Paulina movement
        if keys[pygame.K_LEFT]: 
            paulina_rect.x -= 4
            if paulina_rect.left < screen_rect.left:
                paulina_rect.x = screen_rect.left
        if keys[pygame.K_RIGHT]:
            paulina_rect.x += 4
            if paulina_rect.right > screen_rect.right:
                paulina_rect.x = screen_rect.right - paulina_rect.width
        
        # Drop envelope, stops the obstacles from dropping
        if round_count == ROUNDS:
            falling_objects.append(letter)
            round_count += 1
        # Drops object
        elif round_count < ROUNDS:
            if random.randint(0, 75) < 2:
                falling_objects.append(obstacle())
                round_count += 1
                        
        if len(falling_objects) > 0:
            # Dies
            if paulina_rect.colliderect(falling_objects[0]):
                falling_objects.pop(0)
                game_state = "game_over"

        # Rendering the game
        screen.fill("white")
        screen.blit(bg_img, screen_rect)
        screen.blit(PAULINA_SURFACE, paulina_rect)
        for object in falling_objects:
            if object.rect.y >= GROUND+(object.rect.height):
                falling_objects.remove(object)
                if isinstance(object, envelope):
                    game_state = "landed"
                    print(game_state)
                    object.draw(screen, 0, 0)
                    falling_objects = []
            else:
                object.draw(screen, 0, 6)
        
        #for next time, render envelope opening
    if game_state == "game_over":
        draw_start_menu("L", "press space to restart")
        if keys[pygame.K_SPACE]:
            paulina_rect.x, paulina_rect.y = START_POSITION
            game_state = "game"
            round_count = 0
            paulina_rect.x, paulina_rect.y = START_POSITION
            falling_objects = []

    if game_state == "landed":
        # Paulina movement
        if keys[pygame.K_LEFT]: 
            paulina_rect.x -= 4
            if paulina_rect.left < screen_rect.left:
                paulina_rect.x = screen_rect.left
        if keys[pygame.K_RIGHT]:
            paulina_rect.x += 4
            if paulina_rect.right > screen_rect.right:
                paulina_rect.x = screen_rect.right - paulina_rect.width

        screen.fill("white")
        screen.blit(bg_img, screen_rect)
        screen.blit(PAULINA_SURFACE, paulina_rect)
        letter.draw(screen, 0, 0)

        if paulina_rect.colliderect(letter.rect):
            letter.open(screen)

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()