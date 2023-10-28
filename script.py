#!usr/bin/python3
"""
    These are imported modules for the project.
"""
import random
import pygame
pygame.init()

SCREEN_WIDTH = 864
SCREEN_HEIGHT = 936
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
FPS = 60

bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')

GROUND_SCROLL = 0
SCROLL_SPEED = 4
FLYING = False
GAME_OVER = False
PIPE_GAP = 150
PIPE_FREQUENCY = 1500
LAST_PIPE = pygame.time.get_ticks() - PIPE_FREQUENCY
PASS_PIPE = False
SCORE = 0
white = (255, 255, 255)
font = pygame.font.SysFont('Bauhaus 93', 60)

def draw_text(text, mfont, text_col, x, y):
    """
        This is created to draw the text.
    """
    img = mfont.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    """
        This is created to reset the game.
    """
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(SCREEN_HEIGHT / 2)
    score = 0
    return score

class Bird(pygame.sprite.Sprite):
    """
        This is the Bird class.
    """
    def __init__(self, x, y):
        """
            This is the Bird's init function.
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range (1, 4):
            img = pygame.image.load(f"img/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
    def update(self):
        """
            This is the Bird's update function.
        """
        if FLYING is True:
            self.vel += 0.5
            self.vel = min(self.vel, 8)
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)
        if GAME_OVER is False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            flap_cooldown = 5
            self.counter += 1
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    """
        This is the Pipe class.
    """
    def __init__(self, x, y, position):
        """
            This is Pipe's init function.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(PIPE_GAP / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(PIPE_GAP / 2)]
    def update(self):
        """
            This is Pipe's update function.
        """
        self.rect.x -= SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()

class Button():
    """
        This is the Button class.
    """
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def draw(self):
        """
            This is Button's draw function.
        """
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
flappy = Bird(100, int(SCREEN_HEIGHT / 2))
bird_group.add(flappy)
button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100, button_img)

RUN = True
while RUN:
    clock.tick(FPS)
    screen.blit(bg, (0,0))
    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()
    screen.blit(ground_img, (GROUND_SCROLL, 768))
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and PASS_PIPE is False:
            PASS_PIPE = True
        if PASS_PIPE is True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                SCORE += 1
                PASS_PIPE = False
    draw_text(str(SCORE), font, white, int(SCREEN_WIDTH / 2), 20)
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        GAME_OVER = True
    if flappy.rect.bottom >= 768:
        GAME_OVER = True
        FLYING = False
    if FLYING is True and GAME_OVER is False:
        time_now = pygame.time.get_ticks()
        if time_now - LAST_PIPE > PIPE_FREQUENCY:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, -1)
            top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            LAST_PIPE = time_now
        pipe_group.update()
        GROUND_SCROLL -= SCROLL_SPEED
        if abs(GROUND_SCROLL) > 35:
            GROUND_SCROLL = 0
    if GAME_OVER is True:
        if button.draw():
            GAME_OVER = False
            SCORE = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        if event.type == pygame.MOUSEBUTTONDOWN and FLYING is False and GAME_OVER is False:
            FLYING = True
    pygame.display.update()
pygame.quit()
