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

# FONT
custom_font = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((30, 30)) # how sprite looks in game window
        self.image = pygame.image.load(os.path.join(img_dir, "green circle.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        # self.rect = self.image_scaled.get_rect()

        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision

        self.rect.centerx = 100
        self.rect.bottom = 100
        self.speed_x = 0.0
        self.speed_y = 0.0

        # FIRING DELAY
        self.firing_delay = 100
        self.last_fired = pygame.time.get_ticks()
        # ammo stuff
        self.clip_size = 8
        self.ammo = self.clip_size
        # use for play reload sound only once
        self.reload_a = 0

    def update(self):
        self.textRender(window, str(self.rect.centerx), 25, self.rect.centerx - 50, self.rect.centery + 50)
        self.textRender(window, str(self.rect.centery), 25, self.rect.centerx + 50, self.rect.centery + 50)

        self.speed_x = 0
        self.speed_y = 0
        speed = 2.5

        key_state = pygame.key.get_pressed()
        mouse_state = pygame.mouse.get_pressed()
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

        # NO GOING OUT OF WINDOW
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.top < 0:
            self.rect.top = 0

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
                projectile = Projectile(self.rect.centerx, self.rect.centery, 10, 10)  # MAKE TO CURSOR
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
        projectile = Projectile(self.rect.centerx, self.rect.centery, 50, 10)
        # projectile = Projectile(self.rect.centerx, self.rect.centery, player)
        #     game_sprites.add(projectile)
        #     projectiles.add(projectile)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, coord):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_dir, "red circle.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision

        self.rect.centerx = coord[0]
        self.rect.centery = coord[1]
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.speed = 7

        self.health = 100
        self.display_hurt = False
        self.time_to_stop_display_hurt = 0
        self.time_to_die = 0
        self.oof = 0

    def update(self):
        # collisions GROUP variable, DELETE any projectiles that collide with enemy sprite
        collisions = pygame.sprite.groupcollide(projectiles, enemy_sprites, True, False)

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
            self.textRender(window, str(self.health), 10, self.rect.centerx, self.rect.top - 25)
            # DISPLAY FOR CERTAIN AMT OF TIME
            # time now, time now + length
            # display if (time now) < (time now + length)
            # if time_now < self.time_to_stop_display_hurt:
                # self.textRender(window, "o no i got shot", 30, self.rect.centerx, self.rect.top - 60)
            # else:
                # self.textRender(window, "haha can't shoot me loser", 15, self.rect.centerx, self.rect.top - 50)
        else:
            self.kill()

        if self.oof == 1:
            oof_sound.play()

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
    def __init__(self, x, y, xscale, yscale):
        pygame.sprite.Sprite.__init__(self)
        # self.targ = targ

        mouse_pos = pygame.mouse.get_pos()
        # self.image = pygame.Surface((30, 30)) # how sprite looks in game window
        self.image = pygame.image.load(os.path.join(img_dir, "red circle.png")).convert_alpha()
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



# # game sprite group
# game_sprites = pygame.sprite.Group()
# enemy_sprites = pygame.sprite.Group()
# player_sprites = pygame.sprite.Group()
#
# # create player object
# player = Player()
# enemy = Enemy(600, 50)
# # add sprite to game's sprite group
# game_sprites.add(player)
# game_sprites.add(enemy)
# enemy_sprites.add(enemy)
# player_sprites.add(player)

clock = pygame.time.Clock()

pause_screen = False  # HANDLING PAUSE
title_screen = True


def paused():
    window.fill((0,0,0))
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


global map_screen
map_screen = False


class Bus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_dir, "busD.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision

        self.rect.centerx = 50
        self.rect.bottom = height / 2
        self.speed_x = 0.0
        self.speed_y = 0.0

    def update(self):
        # self.textRender(window, str(self.rect.centerx), 20, self.rect.centerx-50, self.rect.top-25)
        # self.textRender(window, str(self.rect.centery), 20, self.rect.centerx + 50, self.rect.top - 25)

        self.speed_x = 0
        self.speed_y = 0
        speed = 3

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

        if key_state[pygame.K_a]:
            self.image = pygame.image.load(os.path.join(img_dir, "busA.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (70, 70))
        if key_state[pygame.K_d]:
            self.image = pygame.image.load(os.path.join(img_dir, "busD.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (70, 70))


        # NO GOING OUT OF WINDOW
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.top < 0:
            self.rect.top = 0

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




class MapLocation(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([40, 40]) # how sprite looks in game window
        self.image.fill(WHITE)
        # pygame.draw.rect(self.image,WHITE,pygame.Rect(x, y, width, height))
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision

        self.rect.centerx = 500
        self.rect.centery = height / 2

    def update(self):
        # collisions GROUP variable
        collisions = pygame.sprite.groupcollide(bussy, city1group, False, False)
        # when  collides
        if collisions:
            self.textRender(window, "Press SPACE to enter this city.", 15, width / 2, height - 50)
            # for event in pygame.event.get():
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_SPACE:
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

class BusPortal(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_dir, "busD.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision

        self.rect.centerx = width - 100
        self.rect.centery = height - 100

    def update(self):
        # collisions GROUP variable
        collisions = pygame.sprite.groupcollide(player_sprites, bustransport, False, False)
        # when  collides
        if collisions:
            self.textRender(window, "Press SPACE to enter this vehicle.", 15, width / 2, height - 50)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        global map_screen
                        map_screen = True


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

# game sprite group
game_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()

# create player object
player = Player()
# enemy = Enemy(600, 50)
# add sprite to game's sprite group
game_sprites.add(player)
# game_sprites.add(enemy)
# enemy_sprites.add(enemy)
player_sprites.add(player)

bussy = pygame.sprite.Group()
bus = Bus()
bussy.add(bus)

city1group = pygame.sprite.Group()
city1 = MapLocation()
city1group.add(city1)

bustransport = pygame.sprite.Group()
busportal = BusPortal()
bustransport.add(busportal)


def showmap():
    window.fill((138, 98, 65))
    # Create a text surface with "Game is Paused"
    text_surface = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"), 48).render("World Map",
                                                                                                  True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 2, 50)

    # Draw the text surface to the screen
    window.blit(text_surface, text_rect)

spawnfirstenemies = True

def firstlevel():
    # enemy_locations = ([100, 100], [200, 100], [300, 100])
    enemy_locations = (850, 100), (850, 250), (150, 400), (300, 600),
    # for location in enemy_locations:
    #     newEnemy = Enemy(location)
    #     enemy_sprites.add(newEnemy)
    #     game_sprites.add(newEnemy)

    e1 = Enemy(enemy_locations[0])
    e2 = Enemy(enemy_locations[1])
    e3 = Enemy(enemy_locations[2])
    e4 = Enemy(enemy_locations[3])
    enemy_sprites.add(e1)
    enemy_sprites.add(e2)
    enemy_sprites.add(e3)
    enemy_sprites.add(e4)
    game_sprites.add(e1)
    game_sprites.add(e2)
    game_sprites.add(e3)
    game_sprites.add(e4)




while not done:
    time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_p and not map_screen:  # HANDLING PAUSE
                pause_screen = not pause_screen
            if event.key == pygame.K_SPACE and title_screen:
                title_screen = not title_screen
            # if event.key == pygame.K_m and not pause_screen and not title_screen:
            #     map_screen = not map_screen


    # window.fill((0,155,0))

    # HANDLING PAUSE, title, and play states
    if title_screen:
        title()
    elif not (pause_screen or map_screen) :
        if spawnfirstenemies:
            firstlevel()
            spawnfirstenemies = False

        window.fill((0, 155, 0))
        game_sprites.update()
        game_sprites.draw(window)
        bustransport.update()
        bustransport.draw(window)
    elif pause_screen and not map_screen and not title_screen:
        paused()
    elif map_screen and not pause_screen and not title_screen:
        showmap()
        bussy.update()
        bussy.draw(window)
        city1group.update()
        city1group.draw(window)

    clock.tick(60)
    pygame.display.flip()
