import pygame
import os
import random

pygame.init()
width = 1600;
height = 900;
window = pygame.display.set_mode((width, height))
done = False

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

rectX = width/2-30
rectY = height/2-30

game_dir = os.path.dirname(__file__)
assets_dir = os.path.join(game_dir, "assets")
img_dir = os.path.join(assets_dir, "images")

green_circle = pygame.image.load(os.path.join(img_dir, "green circle.png"))
red_circle = pygame.image.load(os.path.join(img_dir, "red circle.png"))

green_circle = pygame.image.load(os.path.join(img_dir, "green circle.png")).convert()
red_circle = pygame.image.load(os.path.join(img_dir, "red circle.png")).convert()

green_circle.set_colorkey(WHITE)
red_circle.set_colorkey(WHITE)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((30, 30)) # how sprite looks in game window
        self.image = pygame.image.load(os.path.join(img_dir, "green circle.png")).convert()
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision
        self.rect.centerx = width / 2
        self.rect.bottom = height - 20
        self.speed_x = 0.0
        self.speed_y = 0.0

    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        speed = 10

        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_a]:
            self.speed_x = -speed
        if key_state[pygame.K_d]:
            self.speed_x = speed
        if key_state[pygame.K_s]:
            self.speed_y = speed
        if key_state[pygame.K_w]:
            self.speed_y = -speed

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.top < 0:
            self.rect.top = 0

    def fire(self):

        mob = Mob(self.rect.centerx, self.rect.top, player)

        game_sprites.add(mob)

        mobs.add(mob)

mobs = pygame.sprite.Group()
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, targ):
        pygame.sprite.Sprite.__init__(self)
        self.targ = targ

        # self.image = pygame.Surface((30, 30)) # how sprite looks in game window
        self.image = pygame.image.load(os.path.join(img_dir, "red circle.png")).convert()
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision

        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        speed = 10

        self.rect.centery -= speed

        # CODE FOR MOB TO FOLLOW PLAYER

        # x_d = self.rect.centerx - self.targ.rect.centerx
        # y_d = self.rect.centery - self.targ.rect.centery
        # dist = (x_d**2 + y_d**2)**.5
        # if dist > 0:
        #     vx = x_d/dist*speed
        #     vy = y_d/dist*speed
        #     if dist > 500:
        #         self.rect.centerx -= vx*3
        #         self.rect.centery -= vy*3
        #     if (dist <= 500) & (dist > 200):
        #         self.rect.centerx -= vx*2
        #         self.rect.centery -= vy*2
        #     if dist <= 200:
        #         self.rect.centerx -= vx
        #         self.rect.centery -= vy



# game sprite group
game_sprites = pygame.sprite.Group()


# create player object
player = Player()
# add sprite to game's sprite group
game_sprites.add(player)

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_SPACE:
                player.fire()

    key_state = pygame.key.get_pressed()
    if key_state[pygame.K_ESCAPE]:
        done = True

    window.fill(BLACK)

    game_sprites.update()
    game_sprites.draw(window)

    pygame.display.flip()
    clock.tick(60)
    pygame.display.flip()

