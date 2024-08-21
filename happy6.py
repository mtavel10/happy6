import pygame
import sys, random, time

# CONSTANTS
WIDTH = 800
HEIGHT = 600
OB_SPEED = 7
ROUNDS = 75
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
bg_img = pygame.transform.scale(pygame.image.load("minecraftbackground.jpg"), 
                                (WIDTH, HEIGHT))
message_file = open("letter.txt", "r")
message_list = message_file.readlines()
message_string = " "
for line in message_list:
    message_string += line

print(message_string)

class obstacle():
    def __init__(self):
        self.SURFACE = pygame.transform.scale(pygame.image.load("tnt.png"), (45, 45))
        self.EXPLODED_SURFACE = pygame.transform.scale(pygame.image.load("explosion.png"), (50, 50))
        self.rect = pygame.Rect(random.randint(0, WIDTH - 100), 0, 45, 45)
        self.exploded = 0
    def draw(self, screen, x=0, y=0):
        self.rect.x += x
        self.rect.y += y
        screen.blit(self.SURFACE, self.rect)
    def explode(self, screen, x=0, y=0):
        self.rect.x += x
        self.rect.y += y
        screen.blit(self.EXPLODED_SURFACE, self.rect)
        self.exploded += 1
    
class envelope():
    def __init__(self):
        self.SURFACE = pygame.transform.scale(pygame.image.load("envelope.png"), (65, 40))
        self.rect = pygame.Rect(WIDTH/2, 0, 50, 50)
        self.back = ""
    def draw(self, screen, x=0, y=0):
        self.rect.x += x
        self.rect.y += y
        screen.blit(self.SURFACE, self.rect)
    def open(self, screen):
        font = pygame.font.SysFont('arial', 18)
        msg_rect = pygame.Rect(WIDTH/11, HEIGHT/11, WIDTH - (WIDTH/5), HEIGHT - (HEIGHT/5))
        self.back = drawText(screen, message_string, "black", msg_rect, font, bkg="white")
    def flip(self, screen):
        font = pygame.font.SysFont('arial', 30)
        msg_rect = pygame.Rect(WIDTH/8, HEIGHT/8, WIDTH - (WIDTH/4), HEIGHT - (HEIGHT/4))
        drawText(screen, self.back, "black", msg_rect, font, False, "white")
        screen.blit(screen, msg_rect)

def draw_start_menu(message1: str, message2: str):
    screen.fill("white")
    screen.blit(bg_img, screen_rect)
    font = pygame.font.SysFont('arial', 40)
    title = font.render(message1, True, "black")
    start_button = font.render(message2, True, "black")
    screen.blit(title, (WIDTH/2 - title.get_width()/2, HEIGHT/2 - title.get_height()/2))
    screen.blit(start_button, (WIDTH/2 - start_button.get_width()/2, HEIGHT/2 + start_button.get_height()/2))
    pygame.display.update()

# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight >= rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] <= rect.width and i <= len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i <= len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text


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
            if random.randint(0, 50) < 2:
                falling_objects.append(obstacle())
                round_count += 1
                        
        if len(falling_objects) > 0:
            # Dies
            collided = falling_objects[0]
            if paulina_rect.colliderect(collided):
                if isinstance(collided, envelope): 
                    game_state = "landed"
                else: 
                    falling_objects.pop(0)
                    game_state = "game_over"

        # Rendering the game
        screen.fill("white")
        screen.blit(bg_img, screen_rect)
        screen.blit(PAULINA_SURFACE, paulina_rect)
        for object in falling_objects:
            # If the object hit the ground
            if object.rect.top >= GROUND+(object.rect.height):
                if isinstance(object, envelope):
                    game_state = "landed"
                    object.draw(screen, 0, 0)
                    falling_objects = []
                else: 
                    object.explode(screen, 0, 6)
                    # the number of frames I want to explosion to stay
                    if object.exploded >= 5: 
                        falling_objects.remove(object)
                    else: 
                        object.explode(screen, 0, 0)
            else:
                object.draw(screen, 0, 6)
        
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
            # blit two arrows
            letter.open(screen)

            # if keys[pygame.K_a]: 
            #     letter.flip(screen)
            # if keys[pygame.K_d]:
            #     letter.flip (screen)
                
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()