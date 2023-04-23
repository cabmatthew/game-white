import pygame
import os

pygame.init()
width = 1000;
height = 700;
window = pygame.display.set_mode((width, height))
done = False

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

rectX = width / 2 - 30
rectY = height / 2 - 30

game_dir = os.path.dirname(__file__)
assets_dir = os.path.join(game_dir, "assets")
img_dir = os.path.join(assets_dir, "images")
fnt_dir = os.path.join(assets_dir, "fonts")

# Importing images for sprites & bullets
green_circle = pygame.image.load(os.path.join(img_dir, "green circle.png")).convert()
red_circle = pygame.image.load(os.path.join(img_dir, "red circle.png")).convert()

green_circle.set_colorkey(WHITE)
red_circle.set_colorkey(WHITE)

# SOUNDS
pygame.mixer.init()
snd_dir = os.path.join(assets_dir, "sounds")
pew_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'pew.wav'))
oof_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'oof.wav'))
reload_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'reload.wav'))

#######
scene = [
    "XXXXXXXXXXXXXXXXXXXXXX",
    "X--------------------X",
    "X--------------------X",
    "X--------------------X",
    "XXXXXXXX-------------X",
    "X--------------------X",
    "X------X-------------X",
    "X--XX--XXXXXXXXXXXXXXX",
    "X--XX--X-------------X",
    "X--------------------X",
    "X------X-------------X",
    "XXXXXXXXXXXXXXXXXXXXXX"]
#
mappa = pygame.Surface((len(scene[0]) * 64, len(scene) * 64))
x, y = 0, 0
for row in scene:
    for tile in row:
        if tile in "-":
            pygame.draw.rect(mappa, (0, 155, 0), ((x, y), (64, 64)))
        elif tile in "X":
            pygame.draw.rect(mappa, (125, 125, 125), ((x, y), (64, 64)))
        else:
            pygame.draw.rect(mappa, (255, 128, 122), ((x, y), (64, 64)))
        x += 64
    y += 64
    x = 0
##########


# FONT
custom_font = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((30, 30)) # how sprite looks in game window
        self.image = pygame.image.load(os.path.join(img_dir, "green circle.png")).convert()
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (50, 50))
        # self.rect = self.image_scaled.get_rect()

        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision

        self.rect.centerx = width / 2
        self.rect.bottom = height - 20
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.speed = 5

        # FIRING DELAY
        self.firing_delay = 100
        self.last_fired = pygame.time.get_ticks()
        # ammo stuff
        self.clip_size = 8
        self.ammo = self.clip_size
        # use for play reload sound only once
        self.reload_a = 0

        ##############
        self.map_pos = (0, 0)
        self.moveBox = (100, 100, 900, 600)
        #############

    def update(self):
        ###
        mx, my = self.map_pos

        ####
        self.speed_x = 0
        self.speed_y = 0

        key_state = pygame.key.get_pressed()
        mouse_state = pygame.mouse.get_pressed()
        if key_state[pygame.K_a]:
            self.speed_x = -self.speed
        if key_state[pygame.K_d]:
            self.speed_x = self.speed
        if key_state[pygame.K_s]:
            self.speed_y = self.speed
        if key_state[pygame.K_w]:
            self.speed_y = -self.speed

        # if (self.map_pos[0] < 105):
        #     self.speed_x = 0

        # if (self.map_pos[1] < 105):
        #     self.speed_y = 0

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        ####### IN FUTURE, STOP MOVEMENT WHEN COLLIDING WITH WALL
        if player.rect.x <= self.moveBox[0]:
            self.rect.x += self.speed
            if self.map_pos[0] < 105:  ### HANDLING REACHING MAP BORDER
                mx += self.speed
        elif player.rect.x >= self.moveBox[2] - 32:
            self.rect.x -= self.speed
            if self.map_pos[0] > -490:
                mx -= self.speed
        if player.rect.y <= self.moveBox[1]:
            self.rect.y += self.speed
            if self.map_pos[1] < 105:
                my += self.speed
        elif player.rect.y >= self.moveBox[3] - 32:
            self.rect.y -= self.speed
            if self.map_pos[1] > -150:
                my -= self.speed
        self.map_pos = (mx, my)

        self.render(window)
        ##########

        # FIRING
        if mouse_state[0]:
            self.fire()

        # RELOADING
        if key_state[pygame.K_r]:
            self.reload()
            # stuff to have reload sound just once
            self.reload_a += 1
            if self.reload_a == 1:
                reload_sound.play()

        # AMMO TEXT
        self.textRender(window, str(self.ammo), 20, 30, 10)
        self.textRender(window, "/", 20, 50, 10)
        self.textRender(window, str(self.clip_size), 20, 70, 10)
        if self.ammo == 0:
            self.textRender(window, "trash player got no ammo, RELOAD", 25, width / 2, 80)

        # SHOWING LOCATION IN MAP
        self.textRender(window, str(self.map_pos), 30, self.rect.centerx, self.rect.top - 60)

        # todo ask matt if this is needed anymore
        # NO GOING OUT OF WINDOW
        # if self.rect.right > width:
        #     self.rect.right = width
        # if self.rect.left < 0:
        #     self.rect.left = 0
        # if self.rect.bottom > height:
        #     self.rect.bottom = height
        # if self.rect.top < 0:
        #     self.rect.top = 0
        # if self.map_pos[0] < 100:
        #     self.rect.x = 100
        # if self.map_pos[1] < 0:
        #     self.rect.y = 0
        # if self.map_pos[0] > 800:
        #     self.rect.x = 799
        # if self.map_pos[1] > 700:
        #     self.rect.y = 699

    #########
    def render(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    ##########
    def fire(self):
        # get current time
        time_now = pygame.time.get_ticks()

        # fire at rate of self.firing_delay
        # fire only if ammo available
        if self.ammo > 0:
            # if time between last shot and now is MORE than delay, FIRE
            if time_now - self.last_fired > self.firing_delay:
                # update time of last fired shot
                self.last_fired = time_now
                # spawn projectile
                mouse_pos = pygame.mouse.get_pos()
                projectile = Projectile(self.rect.centerx, self.rect.centery, enemy, 10, 10)  # MAKE TO CURSOR
                # projectile = Projectile(mouse_pos[0], mouse_pos[1], enemy, 10, 10)  # MAKE TO CURSOR
                game_sprites.add(projectile)
                projectiles.add(projectile)
                # use 1 ammo, play pew
                self.ammo -= 1
                pew_sound.play()
        # used to make reload sound play just once, RESET reload ct when firing
        self.reload_a = 0

    def reload(self):
        self.ammo = self.clip_size

    def textRender(self, surface, text, size, x, y):
        # font_match = pygame.font.match_font('arial')
        # specify font for text render - uses found font and size of text
        font = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"), size)
        # surface for text pixels - TRUE = anti-aliased
        text_surface = font.render(text, True, WHITE)
        # get rect for text surface rendering
        text_rect = text_surface.get_rect()
        # specify a relative location for text
        text_rect.midtop = (x, y)
        # add text surface to location of text rect
        surface.blit(text_surface, text_rect)

    def meleeHit(self):
        projectile = Projectile(self.rect.centerx, self.rect.centery, enemy, 50, 10)
        # projectile = Projectile(self.rect.centerx, self.rect.centery, player)
        #     game_sprites.add(projectile)
        #     projectiles.add(projectile)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        # configures mob sprite image that will be seen in the game
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_dir, "red circle.png")).convert()
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision
        # coordinates for the mobs in the game
        self.rect.centerx = width / 2
        self.rect.bottom = height - 20
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.speed = 1
        self.map_pos = (0, 0)
        self.move_box = (100, 100, 900, 600)
        # health
        self.health = 30  # initially set to 100
        self.display_hurt = False
        self.time_to_stop_display_hurt = 0
        self.oof = 0


    def update(self):
        self.mx, self.my = self.map_pos
        self.speed_x = 0.0
        self.speed_y = 0.0
        # todo remove main prefix
        player_x, player_y = player.map_pos

        if player.rect.x > self.rect.x:
            self.speed_x = self.speed
        if player.rect.y > self.rect.y:
            self.speed_y = self.speed
        if player.rect.x < self.rect.x:
            self.speed_x = -self.speed
        if player.rect.y < self.rect.y:
            self.speed_y = -self.speed

        # move speed units every update
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # stop when reaching window boundary
        if self.rect.x <= self.move_box[0]:
            self.rect.x += self.speed
            if self.map_pos[0] < 105:  ### HANDLING REACHING MAP BORDER
                self.mx += self.speed
        elif self.rect.x >= self.move_box[2] - 32:
            self.rect.x -= self.speed
            if self.map_pos[0] > -490:
                self.mx -= self.speed
        if self.rect.y <= self.move_box[1]:
            self.rect.y += self.speed
            if self.map_pos[1] < 105:
                self.my += self.speed
        elif self.rect.y >= self.move_box[3] - 32:
            self.rect.y -= self.speed
            if self.map_pos[1] > -150:
                self.my -= self.speed
        self.map_pos = (self.mx, self.my)

        self.render(window)

        # collisions GROUP variable, DELETE any projectiles that collide with enemy sprite
        collisions = pygame.sprite.groupcollide(enemy_sprites, projectiles, False, True)

        time_now = pygame.time.get_ticks()
        # when ENEMY collides with any PROJECTILE
        if collisions:
            oof_sound.play()
            # SET TIME to stop displaying hurt text
            self.time_to_stop_display_hurt = time_now + 600
            self.health -= 10

        # if ALIVE aka health above 0
        if self.health > 0:
            # when alive, display health
            self.textRender(window, str(self.health), 20, self.rect.centerx, self.rect.top - 25)
            # DISPLAY FOR CERTAIN AMT OF TIME
            # time now, time now + length
            # display if (time now) < (time now + length)
            if time_now < self.time_to_stop_display_hurt:
                self.textRender(window, "o no i got shot", 30, self.rect.centerx, self.rect.top - 60)
            else:
                self.textRender(window, "haha can't shoot me loser", 15, self.rect.centerx, self.rect.top - 50)
        else:
            self.textRender(window, "rip im dead", 60, self.rect.centerx, self.rect.top - 50)
            self.speed = 0
            self.oof += 1

        if self.oof == 1:
            oof_sound.play()

    # def fire(self):
    #
    #     projectile = Projectile(self.rect.centerx, self.rect.centery, player)
    #     game_sprites.add(projectile)
    #     projectiles.add(projectile)

    def render(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def textRender(self, surface, text, size, x, y):
        # specify font for text render - uses found font and size of text
        font = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"), size)
        # surface for text pixels - TRUE = anti-aliased
        text_surface = font.render(text, True, WHITE)
        # get rect for text surface rendering
        text_rect = text_surface.get_rect()
        # specify a relative location for text
        text_rect.midtop = (x, y)
        # add text surface to location of text rect
        surface.blit(text_surface, text_rect)


projectiles = pygame.sprite.Group()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, targ, xscale, yscale):
        pygame.sprite.Sprite.__init__(self)
        self.targ = targ

        mouse_pos = pygame.mouse.get_pos()
        # self.image = pygame.Surface((30, 30)) # how sprite looks in game window
        self.image = pygame.image.load(os.path.join(img_dir, "red circle.png")).convert()
        self.image.set_colorkey(BLACK)
        # self.image.fill(WHITE)
        self.image = pygame.transform.scale(self.image, (xscale, yscale))
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision

        self.rect.centerx = x
        self.rect.bottom = y

        self.speed = 15
        # finding x & y distance
        # x_d = self.rect.centerx - self.targ.rect.centerx
        # y_d = self.rect.centery - self.targ.rect.centery
        x_d = self.rect.centerx - mouse_pos[0]
        y_d = self.rect.centery - mouse_pos[1]
        dist = (x_d ** 2 + y_d ** 2) ** .5
        # calculating velocity x & y components from distance
        self.speed_x = x_d / dist * self.speed
        self.speed_y = y_d / dist * self.speed

        # self.time_alive = time_alive

    def update(self):
        self.rect.centerx -= self.speed_x
        self.rect.centery -= self.speed_y

        if self.rect.right > width:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.bottom > height:
            self.kill()
        if self.rect.top < 0:
            self.kill()


# game sprite group
game_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()

# create player object
player = Player()
enemy = Enemy()
# add sprite to game's sprite group
game_sprites.add(player)
game_sprites.add(enemy)
enemy_sprites.add(enemy)

clock = pygame.time.Clock()

pause_screen = False  # HANDLING PAUSE
title_screen = True


def paused():
    # Create a text surface with "Game is Paused"
    text_surface = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"), 48).render("Game is Paused",
                                                                                                  True, (255, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 2, height // 2)

    # Draw the text surface to the screen
    window.blit(text_surface, text_rect)

    # Update the screen
    pygame.display.flip()


def title():
    title_text = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"), 80).render("Daybreak", True,
                                                                                                BLACK)
    subtitle_text = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"), 15).render("Press [SPACEBAR] "
                                                                                                   "To Start", True,
                                                                                                   BLACK)
    title_background = pygame.image.load(os.path.join(img_dir, "title_bckgnd.png"))
    title_background = pygame.transform.scale(title_background, (width, height))
    title_rect = title_text.get_rect()
    subtitle_rect = subtitle_text.get_rect()
    title_rect.center = (width / 2, height / 2)
    subtitle_rect.center = (width / 2, height / 2 + 70)
    window.blit(title_background, (0, 0))
    window.blit(title_text, title_rect)
    window.blit(subtitle_text, subtitle_rect)
    pygame.display.flip()


while not done:
    time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_p:  # HANDLING PAUSE
                pause_screen = not pause_screen
            if event.key == pygame.K_SPACE and title_screen:
                title_screen = not title_screen
                pygame

    key_state = pygame.key.get_pressed()
    if key_state[pygame.K_ESCAPE]:
        done = True

    window.fill(BLACK)

    # HANDLING PAUSE
    if title_screen:
        title()
    elif not pause_screen:
        window.fill((0, 155, 0))
        window.blit(mappa, player.map_pos)
        player.render(window)

        game_sprites.update()
        game_sprites.draw(window)
    else:
        paused()

    pygame.display.flip()
    clock.tick(60)
    pygame.display.flip()
