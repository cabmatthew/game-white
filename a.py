import pygame, sys

# Color definitions
BLUE = (10, 10, 128)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
# Screen width

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([50, 45])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.score = 0

        self.change_x = 0
        self.change_y = 0
        self.walls = None

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self):
        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:

            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom


class Player2(pygame.sprite.Sprite):
    def __init__(self, x, y, human):
        super().__init__()
        self.human = human
        self.image = pygame.Surface([50, 45])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.score = 0

        self.rect.x = 400
        self.rect.y = 40

        self.change_x = 0
        self.change_y = 0
        self.walls = None

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self):
        if self.human.rect.x > self.rect.x:
            self.rect.x += 1
        if self.human.rect.x < self.rect.x:
            self.rect.x -= 1
        if self.human.rect.y > self.rect.y:
            self.rect.y += 1
        if self.human.rect.y < self.rect.y:
            self.rect.y -= 1


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


# Wall init

wall_list = pygame.sprite.Group()

# Pygame definitions

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('test!')
all_sprite_list = pygame.sprite.Group()

# Left wall
wall = Wall(0, 0, 10, 600)
wall_list.add(wall)
all_sprite_list.add(wall)
# top wall
wall = Wall(10, 0, 790, 10)
wall_list.add(wall)
all_sprite_list.add(wall)

# Right wall
wall = Wall(790, 0, 10, 600)
wall_list.add(wall)
all_sprite_list.add(wall)

# Bottom wall
wall = Wall(0, 590, 1000, 300)
wall_list.add(wall)
all_sprite_list.add(wall)

# Create the player
player = Player(50, 50)
all_sprite_list.add(player)
player.walls = wall_list

player2 = Player2(50, 50, player)
all_sprite_list.add(player2)
player2.walls = wall_list

clock = pygame.time.Clock()

# Loop

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_d:
                player.changespeed(3, 0)
            elif event.key == pygame.K_w:
                player.changespeed(0, -3)
            elif event.key == pygame.K_s:
                player.changespeed(0, 3)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.changespeed(3, 0)
            elif event.key == pygame.K_d:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_w:
                player.changespeed(0, 3)
            elif event.key == pygame.K_s:
                player.changespeed(0, -3)

    all_sprite_list.update()
    screen.fill(BLACK)
    all_sprite_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)
    pygame.display.flip()

pygame.quit()